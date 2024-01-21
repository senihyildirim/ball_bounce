# Ball Bounce Counter with OpenCV

## Overview

The "Ball Bounce Counter with OpenCV" project is a Python-based application that leverages the OpenCV library to perform a straightforward yet effective task: counting the number of times a ball bounces on the ground within a given video. This project has been designed to offer a practical example of utilizing computer vision techniques for motion analysis and object tracking.

## Dependencies

To run this project, the following dependencies are required:

- Python 3.7
- OpenCV 4.1.2
- NumPy 1.18.1
- imutils
- collections
- time

## How the Code Works

The core functionality of this project can be broken down into several key steps:

1. **Color Detection**: The first step involves specifying two color ranges, `greenLower` and `greenUpper`, which define the color of the bouncing ball. These color ranges effectively narrow down the spectrum of colors that the program will consider as the ball.

2. **Video Input**: The program accepts a video stream as its input source. Two video files, "two_balls.MOV" and "one_ball.MOV," are provided as options for users. By uncommenting the appropriate line in the code, users can select which video they wish to analyze. A brief waiting period, achieved through `time.sleep(2.0)`, allows the video stream to initialize properly.

3. **Video Processing**: Every frame from the video stream undergoes preprocessing. Gaussian blur is applied to each frame, reducing noise and enhancing the quality of subsequent operations.

4. **Ball Detection**: The heart of the project involves detecting the  ball's presence within each frame. To achieve this, a mask is created that isolates the color. This mask effectively distinguishes the ball from the rest of the colors in the frame. To improve the mask's quality, erosion and dilation operations are applied.

5. **Bounce Count Computation**: The project employs two deque structures, `pts1` and `pts2`, to monitor the bounce counts and motion directions of both the first ball and a secondary ball (if present). When a ball is in proximity to `center1` and has not yet been assigned to `center2`, it is considered for updating `center1` and is added to the `pts1` deque. In the absence of a defined `center2` and when a ball is distanced from `center1`, the ball is designated as `center2`, and it is subsequently added to the `pts2` deque.

6. **Resultant Video Output**: The project culminates in the generation of an output video file. This file visually showcases the detected ball and overlays the calculated bounce count. This visual representation is valuable for both debugging and final output presentation.

7. **Requirements**: To ensure the proper execution of the project, the README specifies the required Python version and necessary libraries. Users must verify that their Python environment complies with these prerequisites.

## Potential Issues

- It is crucial to note that this code is optimized for detecting specific balls within particular environments. Consequently, the accuracy of the code may vary across different settings. The effectiveness of the code hinges on the correct definition of the ball's color range using `greenLower` and `greenUpper`. Depending on the lighting conditions and ball color, these ranges may require fine-tuning.

- As this project does not incorporate a machine learning model, its accuracy heavily relies on the precise definition of the ball's color range using `greenLower` and `greenUpper`. Adjusting these ranges may be necessary to optimize performance.

- The absence of a machine learning model may result in the detection of various objects within the environment. This could potentially lead to inaccurate bounce counting in scenarios where multiple objects share similar colors with the ball.

- This is a static project.

This detailed explanation provides an in-depth understanding of how the "Ball Bounce Counter with OpenCV" project functions and outlines potential challenges that users may encounter.
