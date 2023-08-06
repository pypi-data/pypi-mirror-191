
"""Tools to asses the progress on (road) construction sites."""

import numpy as np
import open3d as o3d
import geomapi.utils as ut
import geomapi.utils.geometryutils as gmu
from typing import List,Tuple
from colour import Color
from geomapi.nodes import ImageNode
import copy 

def assign_point_cloud_information(source_cloud:o3d.geometry.PointCloud,ref_clouds:List[o3d.geometry.PointCloud],class_names:List[int]=None)->np.array:
    ref_cloud,ref_arr=gmu.create_identity_point_cloud(ref_clouds)
    indices,distances=gmu.compute_nearest_neighbors(np.asarray(source_cloud.points),np.asarray(ref_cloud.points))
    index=ref_arr[indices]
    distances=distances[:,0]
    class_names=np.argmax(ref_arr)      if class_names is None  else class_names
    arr=np.zeros(len(np.asarray(source_cloud.points)))
    for ind in np.unique(index):
        locations=np.where(index ==ind)
        np.put(arr,locations,class_names[ind])
    return arr

def filter_img_classifcation_by_neighbors (predictions:np.array,shape: Tuple[int,int]=None,weight:float=3)->np.array:
    """Filters an initial raster prediction based on the classification of surrounding values.\n
    Every value is replaced by the most occuring value in the 9 surrounding raster values weighted by the initial value

    Args:
        predictions (np.array): _description_
        shape (Tuple[int,int]): shape of the raster
        weight (float, optional): influence of the initial value compared to neighboring values. Defaults to 3.

    Returns:
        np.array: _description_
    """
    #validate inputs
    shape=predictions.shape    if not shape     else shape
    predictions=np.reshape(predictions,shape)
    newPredictions=predictions
    #select most frequently occuring value in vincinity of each region (multiplied by weight for initial pixel)
    for i in range(1,predictions.shape[0]-1):
        for j in range(1,predictions.shape[1]-1):
            arr=np.hstack((predictions[i-1:i+1,j-1:j+1].flatten(),np.full((weight-1),predictions[i,j])))         
            newPredictions[i,j]=np.argmax(np.bincount(arr)) 
    return np.reshape(newPredictions,(-1,1)).flatten()
    
def project_pcd_to_rgbd_images (pointClouds:List[o3d.geometry.Geometry], imgNodes:List[ImageNode], depth_scale:float=1.0,depth_max:float=15)->Tuple[List[np.array],List[np.array],List[np.array]]:
    """Project a set of point cloud geometries given camera parameters. The given

    .. image:: ../../../docs/pics/ractracing1.PNG

    Args:
        1.pointClouds (List[o3d.geometry.PointCloud]): set of o3d point clouds.\n
        2.imgNodes (List[ImageNode]): should contain imageWidth,imageHeight,cartesianTransform and focalLength35mm\n
        3.depth_scale (float, optional): Defaults to 1.0 (real distance).\n
        4.depth_max (float, optional): cut off distance. Defaults to 15m.\n

    Returns:
        Tuple[List[np.array],List[np.array],List[np.array]]: colorImages,depthImages
    """
    #validate point clouds
    pointClouds=ut.item_to_list(pointClouds)
    pointClouds=gmu.join_geometries(pointClouds)
    pcd = o3d.t.geometry.PointCloud.from_legacy(pointClouds)
    colorImages=[]
    depthImages=[]
    #project color and depth from point cloud to images
    for n in ut.item_to_list(imgNodes):
        intrinsic=n.get_intrinsic_camera_parameters().intrinsic_matrix
        extrinsic= np.linalg.inv(n.get_cartesian_transform()) 
        rgbd_reproj = pcd.project_to_rgbd_image(int(n.imageWidth),
                                        int(n.imageHeight),
                                        intrinsic,
                                        extrinsic,
                                        depth_scale=depth_scale,
                                        depth_max=depth_max)
        # reverse order so orientation matches image
        colorImage=np.asarray(rgbd_reproj.color.to_legacy())
        # colorImage=colorImage[::-1,::-1]
        depthImage=np.asarray(rgbd_reproj.depth.to_legacy())
        # depthImage=depthImage[::-1,::-1]
    
        colorImages.append(colorImage)
        depthImages.append(depthImage)
    return colorImages,depthImages
        
def get_average_cartesian_transform_ortho(list):
    i=0
    sum1=0
    sum2=0
    sum3=0
    average1=0
    average2=0
    average3=0
    length=0
    matrix=[]

    while i<len(list):
        sum1+=list[i][0][3]
        sum2+=list[i][1][3]
        sum3+=list[i][2][3]
        i+=1

    length=len(list)

    average1=sum1/length
    average2=sum2/length
    average3=sum3/length

    matrix=np.array([[1,0,0,average1],[0,1,0,average2],[0,0,1,average3],[0,0,0,1]])
    return matrix

def create_xy_grids (geometries:List[o3d.geometry.TriangleMesh], resolution:float=0.1, direction:str='Down')-> np.array:
    """Generates a grid of rays (x,y,z,nx,ny,nz) with a spatial resolution from a set of input meshes.\n

    Args:
        1.geometries (List[o3d.geometry.TriangleMesh]): geometries to generate the grid from. grid will be placed at the highest of the lowest point.\n
        2.resolution (float, optional): XY resolution of the grid. Default stepsize is 0.1m.\n
        3.direction (str, optional): 'Up' or 'Down'. Position and direction of the grid. If 'Down', the grid is placed at the highest point with the orientation looking downards (0,0,-1). Defaults to 'Down'.

    Returns:
        np.array[x*y,6]: grid of arrays (x,y,z,nx,ny,nz)
    """
    rays = []

    for g in geometries:
        # create values
        minBound=g.get_min_bound()
        maxBound=g.get_max_bound()
        x = np.arange(minBound[0], maxBound[0],resolution )
        y = np.arange(minBound[1], maxBound[1], resolution )

        if direction == 'Down':
            z=maxBound[2]
            xx, yy = np.meshgrid(x, y)
            zz=np.full((x.size,y.size),z)
            array = np.zeros((np.size(xx), 6))
            array[:, 0] = np.reshape(xx, -1)
            array[:, 1] = np.reshape(yy, -1)
            array[:, 2] = np.reshape(zz, -1)
            array[:, 3] = np.zeros((xx.size,1))[0]
            array[:, 4] = np.zeros((xx.size,1))[0]
            array[:, 5] = -np.ones((xx.size,1))[0]
            ray = o3d.core.Tensor(array,dtype=o3d.core.Dtype.Float32)
            rays.append(ray)
        else:
            z=minBound[2]
            xx, yy = np.meshgrid(x, y)
            zz=np.full((x.size,y.size),z)
            array = np.zeros((np.size(xx), 6))
            array[:, 0] = np.reshape(xx, -1)
            array[:, 1] = np.reshape(yy, -1)
            array[:, 2] = np.reshape(zz, -1)
            array[:, 3] = np.zeros((xx.size,1))[0]
            array[:, 4] = np.zeros((xx.size,1))[0]
            array[:, 5] = np.ones((xx.size,1))[0]
            ray = o3d.core.Tensor(array,dtype=o3d.core.Dtype.Float32)
            rays.append(ray)
    return rays

def volume_mesh_BIM(depthmapFBIM:np.array, depthmapBimMin:np.array,depthmapBimMax:np.asarray,resolution:float=0.1)-> np.array:
    """Calculate the volume per element , three different options where:
            1) mesh is beneath the bim\n
            2) mesh is above the bim\n
            3) mesh is between the top and bottom of the bim\n

    **NOTE**: heinder, move this to tools

    Args:
        1. depthmapFBIM (np.array[:,1]): The distances between the grid per object and the top of the mesh.\n
        2. depthmapBimMin (np.array[:,1]): The distances between the grid per object and the bottom of the bim.\n
        3. depthmapBimMax (np.array[:,1]): The distances between the grid per object and the top of the bim.\n
        4. resolution (np.array[:,1], optional): Resolution of the grid.Defaults to 0.1m.\n

    Returns:
        array of volumes per bim object 
    """    
    m=0
    volume=[]
    while m<len(depthmapFBIM):
        n=0
        v=0
        while n<len(depthmapFBIM[m]):          
            if abs(depthmapFBIM[m][n])<100 and abs((depthmapBimMin[m][n]).numpy())<100 and abs(depthmapBimMax[m][n])<100:
                if depthmapFBIM[m][n] >= depthmapBimMin[m][n]:
                    d=(0)
                elif depthmapFBIM[m][n] < depthmapBimMax[m][n]:
                    d=((depthmapBimMin[m][n] -depthmapBimMax[m][n]).numpy())
                else: 
                    d=((depthmapBimMin[m][n]-depthmapFBIM[m][n]).numpy())
                v+=(d*resolution*resolution)
            n=n+1
        volume.append(v)
        m=m+1            
    return volume

def volume_theoretical_BIM( depthmapBimMin:np.array,depthmapBimMax:np.asarray,resolution:float=0.1)-> np.array:
    """Calculate the theoretical volume per element (m³).\n

    **NOTE**: heinder, move this to tools
    
    Args:
        1. depthmapFBIM (np.array[:,1]): The distances between the grid per object and the top of the mesh.\n
        2. depthmapBimMin (np.array[:,1]): The distances between the grid per object and the bottom of the bim.\n
        3. resolution (np.array[:,1], optional): Resolution of the grid.Defaults to 0.1m.\n

    Returns:
        array of theoretcial volumes per bim object 
    """  
    m=0
    volume=[]
    while m<len(depthmapBimMin):
        n=0
        v=0
        while n<len(depthmapBimMin[m]):
            if abs((depthmapBimMin[m][n]).numpy())<1000 and abs(depthmapBimMax[m][n])<1000:
                d=abs((depthmapBimMin[m][n] -depthmapBimMax[m][n]).numpy())
                v+=(d*resolution*resolution)
            n=n+1
        volume.append(v)
        m=m+1
    return volume

def calculate_completion(volumeMeshBIM:np.array,volumeBIM:np.array)->np.array:
    """Calculate the percentual completion (%) using the theoretical and practical volumes of the bim objects.

    **NOTE**: heinder, move this to tools

    Args:
        1. volumeMeshBIM (np.array[:,1]): The volume between mesh and BIM.\n
        2. volumeBIM (np.array[:,1]): The theoretical BIM.\n

    Returns:
        array of completness [0-1]"""

    completion=[]
    for i,element in enumerate(volumeMeshBIM): 
        if not volumeBIM[i] == 0:
            completion.append(element/volumeBIM[i])
        else:
            completion.append(None)
    return completion

def color_BIMNode(completion, BIMNodes):
    """Colors the BIM mesh geometries in the computed LOA color    
    
    **NOTE**: heinder, move this to tools
    
    
    Args:
        1. LOAs (_type_): results of the LOA analysis
        2. BIMNodes (List[BIMNode]): List of the BIMNodes in the project
        
    Returns:
        None
    """
    for BIMNode in BIMNodes:
        if BIMNode.resource:
                BIMNode.resource.paint_uniform_color([0.5,0.5,0.5])
    for i,BIMNode in enumerate(BIMNodes):
        if not completion[i] == None:
                if not BIMNode.resource:
                    BIMNode.get_resource()
                if completion[i]>=0.95:
                    BIMNode.resource.paint_uniform_color([0,1,0])
                if completion[i]<0.95:
                    BIMNode.resource.paint_uniform_color([1,1,0])
                if completion[i]<=0.50:
                    BIMNode.resource.paint_uniform_color([1,0.76,0])
                if completion[i]<=0.25:
                    BIMNode.resource.paint_uniform_color([1,0,0])

def remove_edges_volume_calculation(depthmapDifference,pcdFlightMax,distance:int=1):
    """    **NOTE**: heinder, move this to tools

    """
    pcd = pcdFlightMax
    pcd_tree = o3d.geometry.KDTreeFlann(pcd)
    i=0 #0
    list=[]
    while i< len(depthmapDifference):
        if pd.isna(depthmapDifference[i]) == True or np.isinf(depthmapDifference[i]):
            list.append(i)
        i+=1

    for item in list:
        [k, idx, _] = pcd_tree.search_radius_vector_3d(pcd.points[item], distance)
        for x in idx:
            if  not (np.isinf(depthmapDifference[x]) or  pd.isna(depthmapDifference[x])):
                depthmapDifference[x]=np.inf
    return depthmapDifference

def color_pointcloud_by_height(pointcloud: o3d.geometry.PointCloud, heights, buckets: int = 5, hmax:float = 10, buffer:float = 0.03):
    """Colors the resulting point cloud of the LOA analysis in a gradient by distance between the matched points from the reference and the source (very slow)

    **NOTE**: heinder, move this to tools. this is a really crappy function

    Args:
        pointcloud (o3d.geometry.PointCloud): Point cloud from the LOA determination or pointcloud matching its the returned indeces
        heights (nx1 array): Array containing the distances between two matched points
        buckets (int, optional): Number of intervals to be colored in. Defaults to 5.
        dmax (float, optional): Distances higher then this distance will be ignored. Defaults to 10.
        byElement (bool, optional): If the LOA must be computed per element of for the enitre cloud. Defaults to False.
        

    Returns:
        o3d.geometry.PointCloud()
    """
    print(pointcloud)

    pointcloud.paint_uniform_color([1,1,1])

    heights[heights == np.inf] = np.min(heights)
    max = np.nanmax(np.asarray(heights))
    # print(max)
    if max > hmax:
        max = hmax

    heights[heights == -np.inf] = np.min(heights)
    min = np.nanmin(np.asarray(heights))
    # print(min)
    if min < -hmax:
        min = -hmax
    
    interval = max / buckets
    lb = 0
    ub = lb+interval
    green = Color("lightgreen")
    colors = list(green.range_to(Color("darkgreen"),buckets))
    colors = [c.rgb for c in colors]
    bucket=0
    while ub <= max:
        places2 = np.where(np.asarray(heights) <= ub)[0]
        # print(places2)
        places3 = np.where(np.asarray(heights) > lb)[0]
        # print(places3)
        for place2 in places2:
            if place2 in places3:
                np.asarray(pointcloud.colors)[place2] = colors[bucket]
        lb = ub
        ub += interval
        bucket +=1


    interval = np.abs(min / buckets)
    ub = 0
    lb = ub-interval 
    

    red = Color("red")
    colors = list(red.range_to(Color("darkred"),buckets))
    colors = [c.rgb for c in colors]
    bucket=0
    
    while lb > min :
        places2 = np.where(np.asarray(heights) <= ub)[0]
        places3 = np.where(np.asarray(heights) > lb)[0]
        for place2 in places2:
            if place2 in places3:
                np.asarray(pointcloud.colors)[place2] = colors[bucket]
        ub = lb
        lb -= interval
        bucket +=1

    places2 = np.where(np.asarray(heights) <= buffer)[0]
    places3 = np.where(np.asarray(heights) > -buffer)[0]
    for place2 in places2:
        if place2 in places3:
            np.asarray(pointcloud.colors)[place2] = [0.5,0.5,0.5]
    
    return pointcloud

def create_xy_grid (geometry, resolution:float=0.1, direction:str='Down', offset:int=10)-> np.array:
    """Generates a grid of rays (x,y,z,nx,ny,nz) with a spatial resolution from a set of input meshes.\n

    **NOTE**: MB, this is ugly code

    Args:
        1.geometries (List[o3d.geometry.TriangleMesh]): geometries to generate the grid from. grid will be placed at the highest of the lowest point.\n
        2.resolution (float, optional): XY resolution of the grid. Default stepsize is 0.1m. \n
        3.direction (str, optional): 'Up' or 'Down'. Position and direction of the grid. If 'Down', the grid is placed at the highest point with the orientation looking downards (0,0,-1). Defaults to 'Down'.

    Returns:
        np.array[x*y,6]: grid of arrays (x,y,z,nx,ny,nz)
    """       
    # create values
    minBound=geometry.get_min_bound()
    maxBound=geometry.get_max_bound()
    x = np.arange(minBound[0], maxBound[0],resolution )
    y = np.arange(minBound[1], maxBound[1], resolution )

    if direction == 'Down':
        z=maxBound[2]+offset
        xx, yy = np.meshgrid(x, y)
        zz=np.full((x.size,y.size),z)
        array = np.zeros((np.size(xx), 6))
        array[:, 0] = np.reshape(xx, -1)
        array[:, 1] = np.reshape(yy, -1)
        array[:, 2] = np.reshape(zz, -1)
        array[:, 3] = np.zeros((xx.size,1))[0]
        array[:, 4] = np.zeros((xx.size,1))[0]
        array[:, 5] = -np.ones((xx.size,1))[0]
        ray = o3d.core.Tensor(array,dtype=o3d.core.Dtype.Float32)
    else:
        z=minBound[2]-offset
        xx, yy = np.meshgrid(x, y)
        zz=np.full((x.size,y.size),z)
        array = np.zeros((np.size(xx), 6))
        array[:, 0] = np.reshape(xx, -1)
        array[:, 1] = np.reshape(yy, -1)
        array[:, 2] = np.reshape(zz, -1)
        array[:, 3] = np.zeros((xx.size,1))[0]
        array[:, 4] = np.zeros((xx.size,1))[0]
        array[:, 5] = np.ones((xx.size,1))[0]
        ray = o3d.core.Tensor(array,dtype=o3d.core.Dtype.Float32)
    return ray

def get_mesh_intersections(geometry:o3d.geometry.Geometry, grid:np.array)-> np.array:
    """Returns [N , X * Y] matrix of distances between a grid and a set of input geometries. \n

    Args:
        1. geometries (List[o3d.geometry.TriangleMesh]): N geometries to compute the distance to.\n
        2. grid(o3d.core.Tensor): Tensor 
       
    Returns:
        np.array: 2D distance array [N , X * Y]
    """
    # create grid
    rays=grid
    # construct raycastscenes
    scene = o3d.t.geometry.RaycastingScene()
    gl = o3d.t.geometry.TriangleMesh.from_legacy(geometry)
    scene = o3d.t.geometry.RaycastingScene()
    id = scene.add_triangles(gl)
    ans = scene.cast_rays(rays)
    return ans['t_hit'].numpy()

def get_bim_intersections (geometries:List[o3d.geometry.TriangleMesh], rays:np.array)-> np.array:
    """Returns [N , X * Y] matrix of distances between a grid and a set of input geometries. \n

    **NOTE**: don't call this BIM when its just meshes. not enough tensor information. this function appears twice

    Args:
        1.geometries (List[o3d.geometry.TriangleMesh]): N geometries to compute the distance to.\n
        2.grid(o3d.core.Tensor): Tensor 
       
    Returns:
        np.array: 2D distance array [N , X * Y]
    """
    intersections=[]
    scene = o3d.t.geometry.RaycastingScene()
    for i,g in enumerate(geometries):
        gl = o3d.t.geometry.TriangleMesh.from_legacy(g)
        scene = o3d.t.geometry.RaycastingScene()
        scene.add_triangles(gl)
        ans = scene.cast_rays(rays[i])
        intersections.append(ans['t_hit'].numpy())
    return intersections

def get_mesh_intersectionsBIM (geometry, grid:np.array)-> np.array:
    """Returns [N , X * Y] matrix of distances between a grid and a set of input geometries. \n

    **NOTE**: don't call this BIM when its just meshes. not enough tensor information. this function appears twice

    Args:
        1.geometries (List[o3d.geometry.TriangleMesh]): N geometries to compute the distance to.\n
        2.grid(o3d.core.Tensor): Tensor 
       
    Returns:
        np.array: 2D distance array [N , X * Y]
    """
    
    # create grid
    rays=grid
       
    # construct raycastscenes
    scene = o3d.t.geometry.RaycastingScene()

    b=[]

    gl = o3d.t.geometry.TriangleMesh.from_legacy(geometry)
    scene = o3d.t.geometry.RaycastingScene()
    id = scene.add_triangles(gl)


    b=[]
    n=0
    while n<len(grid):
        ans = scene.cast_rays(rays[n])
        b.append(ans['t_hit'].numpy())
        n=n+1

    return b

def get_scene_intersections (geometries:List[o3d.geometry.TriangleMesh],mesh1:o3d.geometry.TriangleMesh , mesh2:o3d.geometry.TriangleMesh,resolution:float=0.1, direction:str='Down')-> np.array:
    """Returns [N , d] matrix of distances between a grid and a set of input geometries. \n

    **NOTE**: don't call this BIM when its just meshes. not enough tensor information. this function appears twice

    Args:
        1.geometries (List[o3d.geometry.TriangleMesh]): N geometries to compute the distance to.\n
        2.grid(o3d.core.Tensor): Tensor 
        
    Returns:
        np.array: 2D distance array [N , d]
    """

    # create grid
    rays=create_xy_grid(geometries,resolution=resolution,direction=direction)
        
    # construct raycastscenes
    scene = o3d.t.geometry.RaycastingScene()

    b=[]
    for g in geometries:
        gl = o3d.t.geometry.TriangleMesh.from_legacy(g)
        scene = o3d.t.geometry.RaycastingScene()
        id = scene.add_triangles(gl)
        ans = scene.cast_rays(rays)
        b.append(ans['t_hit'].numpy())
    
    b=np.asarray(b).T

    distance1=0

    mesh1l = o3d.t.geometry.TriangleMesh.from_legacy(mesh1)
    scene = o3d.t.geometry.RaycastingScene()
    id = scene.add_triangles(mesh1l)
    ans = scene.cast_rays(rays)
    distance1=(np.asarray([ans['t_hit'].numpy()]))

    distance1=distance1.T

    distance2=0
    
    mesh2l = o3d.t.geometry.TriangleMesh.from_legacy(mesh2)
    scene = o3d.t.geometry.RaycastingScene()
    id = scene.add_triangles(mesh2l)
    ans = scene.cast_rays(rays)
    distance2=(np.asarray([ans['t_hit'].numpy()]))

    distance2=distance2.T

    print(b.shape)
    print(distance1.shape)
    print(distance2.shape)

    array=np.block([b,distance1,distance2])
    return array

def get_rays_raycast (geometries, direction:str='Down'):
    """Generates a grid of rays (x,y,z,nx,ny,nz) with a spatial resolution from a set of input meshes.\n

    **NOTE**: move this to tools

    Args:
        1.geometries (List[o3d.geometry.TriangleMesh]): geometries to generate the grid from. grid will be placed at the highest of the lowest point.\n
        2.resolution (float, optional): XY resolution of the grid. Default stepsize is 0.1m.
        3.direction (str, optional): 'Up' or 'Down'. Position and direction of the grid. If 'Down', the grid is placed at the highest point with the orientation looking downards (0,0,-1). Defaults to 'Down'.

    Returns:
        np.array[x*y,6]: grid of arrays (x,y,z,nx,ny,nz)
    """
    rays = []
    for g in geometries:
        # create values
        if direction == 'Down':
            points=np.asarray(g.croppedPcdMax.points)
            # print(len(points))
            zero=np.array([(np.zeros(len(g.croppedPcdMin.points)))]).T
            # print((zero))
            minusOne=np.array([-np.ones(len(g.croppedPcdMin.points))]).T
            ray=np.float32(np.column_stack((points,zero,zero,minusOne)))
            rays.append(ray)
        else:
            points=np.asarray(g.croppedPcdMin.points)
            zero=np.array([np.zeros(len(g.croppedPcdMin.points))]).T
            # print(len(zero))
            plusOne=np.array([np.ones(len(g.croppedPcdMin.points))]).T
            ray=np.float32(np.column_stack((points,zero,zero,plusOne)))
            rays.append(ray)
    return rays 

def determine_percentage_of_coverage(sources: List[o3d.geometry.TriangleMesh], reference:o3d.geometry.PointCloud,threshold:float=0.1)-> np.array:
    """Returns the Percentage-of-Coverage (PoC) of every source geometry when compared to a reference geometry. The PoC is defined as the ratio of points on the boundary surface of the source that lie within a Euclidean distance threshold hold of the reference geometry. sampled point cloud on the boundary surface of the sources with a resolution of e.g. 0.1m. \n

    .. math::
        P_{i'}=\{ p|\forall p \in P_i : p_i \cap N\backslash  n_i \} 
        c_i = \frac{|P_{i'}|}{|P_i|}
    
    E.g. a mesh of a beam of which half the surface lies within 0.1m of a point cloud will have a PoC of 0.5.
    
    Args:
        1. sources (o3d.geometry.TriangleMesh/PointCloud): geometries to determine the PoC for. \n
        2. reference (o3d.geometry.PointCloud): reference geometry for the Euclidean distance calculations.\n
        3. threshold (float, optional): sampling resolution of the boundary surface of the source geometries. Defaults to 0.1m.\n

    Raises:
        ValueError: Sources must be o3d.geometry (PointCloud or TriangleMesh)

    Returns:
        List[percentages[0-1.0]] per source
    """
    #if no list, list
    sources=ut.item_to_list(sources)
    sourcePCDs=[]
    indentityArray=None
    percentages=[0.0]*len(sources)

    # check whether source and reference are close together to minize calculations
    ind=gmu.get_box_inliers(reference.get_oriented_bounding_box(), [geometry.get_oriented_bounding_box() for geometry in sources])
    if not ind:
        return percentages

    # sample o3d.geometry and create identitylist so to track the indices.
    for i,source in enumerate(sources):  
        if i in ind:      
            if 'PointCloud' in str(type(source)) :
                sourcePCD=source.voxel_down_sample(threshold)
                indentityArray=np.vstack((indentityArray,np.full((len(sourcePCD.points), 1), i)))
            elif 'TriangleMesh' in str(type(source)):
                area=source.get_surface_area()
                count=int(area/(threshold*threshold))
                sourcePCD=source.sample_points_uniformly(number_of_points=count)
                indentityArray=np.vstack((indentityArray,np.full((len(sourcePCD.points), 1), i)))
            sourcePCDs.append(sourcePCD)
        else:
            sourcePCDs.append(None)

    indentityArray=indentityArray.flatten()
    indentityArray=np.delete(indentityArray,0)

    #compute distances
    joinedPCD=gmu.join_geometries(sourcePCDs)
    distances=joinedPCD.compute_point_cloud_distance(reference)

    #remove distances > threshold
    ind=np.where(np.asarray(distances) <= threshold)[0]
    if ind.size ==0:
        return percentages
    indexArray=[indentityArray[i] for i in ind.tolist()]

    #count occurences
    unique_elements, counts_elements = np.unique(indexArray, return_counts=True)
    for i,n in enumerate(unique_elements):
        percentages[n]=counts_elements[i]/len(sourcePCDs[n].points)
    return percentages
