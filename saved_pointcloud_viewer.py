import cv2
import numpy as np
import open3d as o3d

def load_pointcloud(ply_file):
    pcd = o3d.io.read_point_cloud(ply_file)
    points = np.asarray(pcd.points)
    # Check if the point cloud has colors
    if len(pcd.colors) > 0:
        colors = np.asarray(pcd.colors)
    else:
        colors = np.ones((points.shape[0], 3))  # default to white
    return points, colors

def project_points(points, colors, width=640, height=480):
    # Simple orthographic projection for visualization
    # Normalize points to fit in the image
    min_vals = points.min(axis=0)
    max_vals = points.max(axis=0)
    scale = min(width / (max_vals[0] - min_vals[0]), height / (max_vals[1] - min_vals[1])) * 0.9
    pts_2d = points[:, :2] - min_vals[:2]
    pts_2d *= scale
    pts_2d = pts_2d.astype(np.int32)
    pts_2d[:, 0] = np.clip(pts_2d[:, 0], 0, width - 1)
    pts_2d[:, 1] = np.clip(pts_2d[:, 1], 0, height - 1)
    img = np.zeros((height, width, 3), dtype=np.uint8)
    if colors.shape[1] == 3:
        colors = (colors * 255).astype(np.uint8)
    else:
        colors = np.full((points.shape[0], 3), 255, dtype=np.uint8)
    for pt, color in zip(pts_2d, colors):
        cv2.circle(img, tuple(pt), 1, color.tolist(), -1)
    return img

def main():
    ply_file = "out.ply"  # Change to your .ply file path
    points, colors = load_pointcloud(ply_file)
    img = project_points(points, colors)
    cv2.imshow("PointCloud Viewer", img)
    print("Press any key to exit.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()