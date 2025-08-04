from flask import config
import pyrealsense2 as rs
import numpy as np
import os

def save_pointcloud_to_ply(filename):
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)

    # Start streaming
    pipeline.start(config)

    try:
        # Wait for a coherent pair of frames: depth
        print("Capturing pointcloud...")
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            print("No depth frame captured.")
            return

        # Create pointcloud object
        pc = rs.pointcloud()
        color_frame = frames.get_color_frame()
        if not color_frame:
            print("No color frame captured.")
            return
        # Swap red and blue channels in the color frame
        color_image = np.asanyarray(color_frame.get_data())
        color_image = color_image[:, :, [2, 1, 0]]  # Swap R and B channels
        # Use the original color_frame without modification
        color_frame = frames.get_color_frame()

        pc.map_to(color_frame)  # Map the pointcloud to the color frame

        # Calculate the pointcloud
        points = pc.calculate(depth_frame)

        # Save to PLY file
        print(f"Saving pointcloud to {filename}...")
        points.export_to_ply(filename, color_frame)
        print("Pointcloud saved successfully.")

    finally:
        # Stop streaming
        pipeline.stop()

if __name__ == "__main__":
    output_file = "output.ply"
    save_pointcloud_to_ply(output_file)