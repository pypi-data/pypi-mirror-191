from __future__ import annotations
import photonvision._photonvision
import typing
import ntcore._ntcore
import robotpy_apriltag._apriltag
import wpimath.geometry._geometry

__all__ = [
    "EstimatedRobotPose",
    "LEDMode",
    "Packet",
    "PhotonCamera",
    "PhotonPipelineResult",
    "PhotonPoseEstimator",
    "PhotonTrackedTarget",
    "PhotonUtils",
    "PoseStrategy",
    "RobotPoseEstimator",
    "SimPhotonCamera",
    "SimVisionSystem",
    "SimVisionTarget",
    "target_sort_mode"
]


class EstimatedRobotPose():
    def __init__(self, estimatedPose: wpimath.geometry._geometry.Pose3d, timestamp: seconds) -> None: ...
    @property
    def estimatedPose(self) -> wpimath.geometry._geometry.Pose3d:
        """
        The estimated pose

        :type: wpimath.geometry._geometry.Pose3d
        """
    @estimatedPose.setter
    def estimatedPose(self, arg0: wpimath.geometry._geometry.Pose3d) -> None:
        """
        The estimated pose
        """
    @property
    def timestamp(self) -> seconds:
        """
        The estimated time the frame used to derive the robot pose was taken, in
        the same timebase as the RoboRIO FPGA Timestamp

        :type: seconds
        """
    @timestamp.setter
    def timestamp(self, arg0: seconds) -> None:
        """
        The estimated time the frame used to derive the robot pose was taken, in
        the same timebase as the RoboRIO FPGA Timestamp
        """
    pass
class LEDMode():
    """
    Members:

      kDefault

      kOff

      kOn

      kBlink
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict # value = {'kDefault': <LEDMode.kDefault: -1>, 'kOff': <LEDMode.kOff: 0>, 'kOn': <LEDMode.kOn: 1>, 'kBlink': <LEDMode.kBlink: 2>}
    kBlink: photonvision._photonvision.LEDMode # value = <LEDMode.kBlink: 2>
    kDefault: photonvision._photonvision.LEDMode # value = <LEDMode.kDefault: -1>
    kOff: photonvision._photonvision.LEDMode # value = <LEDMode.kOff: 0>
    kOn: photonvision._photonvision.LEDMode # value = <LEDMode.kOn: 1>
    pass
class Packet():
    """
    A packet that holds byte-packed data to be sent over NetworkTables.
    """
    def __eq__(self, arg0: Packet) -> bool: ...
    @typing.overload
    def __init__(self) -> None: 
        """
        Constructs an empty packet.

        Constructs a packet with the given data.

        :param data: The packet data.
        """
    @typing.overload
    def __init__(self, data: typing.List[int]) -> None: ...
    def __ne__(self, arg0: Packet) -> bool: ...
    def clear(self) -> None: 
        """
        Clears the packet and resets the read and write positions.
        """
    def getData(self) -> typing.List[int]: 
        """
        Returns the packet data.

        :returns: The packet data.
        """
    def getDataSize(self) -> int: 
        """
        Returns the number of bytes in the data.

        :returns: The number of bytes in the data.
        """
    __hash__ = None
    pass
class PhotonCamera():
    """
    Represents a camera that is connected to PhotonVision.ß
    """
    @typing.overload
    def __init__(self, cameraName: str) -> None: 
        """
        Constructs a PhotonCamera from a root table.

        :param instance:   The NetworkTableInstance to pull data from. This can be a
                           custom instance in simulation, but should *usually* be the default
                           NTInstance from {@link NetworkTableInstance::getDefault}
        :param cameraName: The name of the camera, as seen in the UI.
                           over.

        Constructs a PhotonCamera from the name of the camera.

        :param cameraName: The nickname of the camera (found in the PhotonVision
                           UI).
        """
    @typing.overload
    def __init__(self, instance: ntcore._ntcore.NetworkTableInstance, cameraName: str) -> None: ...
    def getCameraName(self) -> str: 
        """
        Returns the name of the camera.
        This will return the same value that was given to the constructor as
        cameraName.

        :returns: The name of the camera.
        """
    def getDriverMode(self) -> bool: 
        """
        Returns whether the camera is in driver mode.

        :returns: Whether the camera is in driver mode.
        """
    def getLEDMode(self) -> LEDMode: 
        """
        Returns the current LED mode.

        :returns: The current LED mode.
        """
    def getLatestResult(self) -> PhotonPipelineResult: 
        """
        Returns the latest pipeline result.

        :returns: The latest pipeline result.
        """
    def getPipelineIndex(self) -> int: 
        """
        Returns the active pipeline index.

        :returns: The active pipeline index.
        """
    def hasTargets(self) -> bool: 
        """
        Returns whether the latest target result has targets.
        This method is deprecated; :meth:`.PhotonPipelineResult.hasTargets` should
        be used instead.

        :deprecated: This method should be replaced with {@link
                     PhotonPipelineResult#HasTargets()}

        :returns: Whether the latest target result has targets.
        """
    def setDriverMode(self, driverMode: bool) -> None: 
        """
        Toggles driver mode.

        :param driverMode: Whether to set driver mode.
        """
    def setLEDMode(self, led: LEDMode) -> None: 
        """
        Sets the LED mode.

        :param led: The mode to set to.
        """
    def setPipelineIndex(self, index: int) -> None: 
        """
        Allows the user to select the active pipeline index.

        :param index: The active pipeline index.
        """
    @staticmethod
    def setVersionCheckEnabled(enabled: bool) -> None: ...
    def takeInputSnapshot(self) -> None: 
        """
        Request the camera to save a new image file from the input
        camera stream with overlays.
        Images take up space in the filesystem of the PhotonCamera.
        Calling it frequently will fill up disk space and eventually
        cause the system to stop working.
        Clear out images in /opt/photonvision/photonvision_config/imgSaves
        frequently to prevent issues.
        """
    def takeOutputSnapshot(self) -> None: 
        """
        Request the camera to save a new image file from the output
        stream with overlays.
        Images take up space in the filesystem of the PhotonCamera.
        Calling it frequently will fill up disk space and eventually
        cause the system to stop working.
        Clear out images in /opt/photonvision/photonvision_config/imgSaves
        frequently to prevent issues.
        """
    @property
    def _driverModePublisher(self) -> ntcore._ntcore.BooleanPublisher:
        """
        :type: ntcore._ntcore.BooleanPublisher
        """
    @property
    def _driverModeSubscriber(self) -> ntcore._ntcore.BooleanSubscriber:
        """
        :type: ntcore._ntcore.BooleanSubscriber
        """
    @property
    def _inputSaveImgEntry(self) -> ntcore._ntcore.IntegerPublisher:
        """
        :type: ntcore._ntcore.IntegerPublisher
        """
    @property
    def _inputSaveImgSubscriber(self) -> ntcore._ntcore.IntegerSubscriber:
        """
        :type: ntcore._ntcore.IntegerSubscriber
        """
    @property
    def _ledModePub(self) -> ntcore._ntcore.IntegerPublisher:
        """
        :type: ntcore._ntcore.IntegerPublisher
        """
    @property
    def _ledModeSub(self) -> ntcore._ntcore.IntegerSubscriber:
        """
        :type: ntcore._ntcore.IntegerSubscriber
        """
    @property
    def _ledModeSubscriber(self) -> ntcore._ntcore.IntegerSubscriber:
        """
        :type: ntcore._ntcore.IntegerSubscriber
        """
    @property
    def _m_topicNameSubscriber(self) -> ntcore._ntcore.MultiSubscriber:
        """
        :type: ntcore._ntcore.MultiSubscriber
        """
    @property
    def _mainTable(self) -> ntcore._ntcore.NetworkTable:
        """
        :type: ntcore._ntcore.NetworkTable
        """
    @property
    def _outputSaveImgEntry(self) -> ntcore._ntcore.IntegerPublisher:
        """
        :type: ntcore._ntcore.IntegerPublisher
        """
    @property
    def _outputSaveImgSubscriber(self) -> ntcore._ntcore.IntegerSubscriber:
        """
        :type: ntcore._ntcore.IntegerSubscriber
        """
    @property
    def _packet(self) -> Packet:
        """
        :type: Packet
        """
    @property
    def _path(self) -> str:
        """
        :type: str
        """
    @property
    def _pipelineIndexPub(self) -> ntcore._ntcore.IntegerPublisher:
        """
        :type: ntcore._ntcore.IntegerPublisher
        """
    @property
    def _pipelineIndexSub(self) -> ntcore._ntcore.IntegerSubscriber:
        """
        :type: ntcore._ntcore.IntegerSubscriber
        """
    @property
    def _rawBytesEntry(self) -> ntcore._ntcore.RawSubscriber:
        """
        :type: ntcore._ntcore.RawSubscriber
        """
    @property
    def _rootTable(self) -> ntcore._ntcore.NetworkTable:
        """
        :type: ntcore._ntcore.NetworkTable
        """
    @property
    def _versionEntry(self) -> ntcore._ntcore.StringSubscriber:
        """
        :type: ntcore._ntcore.StringSubscriber
        """
    @property
    def test(self) -> bool:
        """
        :type: bool
        """
    @test.setter
    def test(self, arg0: bool) -> None:
        pass
    @property
    def testResult(self) -> PhotonPipelineResult:
        """
        :type: PhotonPipelineResult
        """
    pass
class PhotonPipelineResult():
    """
    Represents a pipeline result from a PhotonCamera.
    """
    def __eq__(self, arg0: PhotonPipelineResult) -> bool: ...
    @typing.overload
    def __init__(self) -> None: 
        """
        Constructs an empty pipeline result.

        Constructs a pipeline result.

        :param latency: The latency in the pipeline.
        :param targets: The list of targets identified by the pipeline.
        """
    @typing.overload
    def __init__(self, latency: seconds, targets: typing.List[PhotonTrackedTarget]) -> None: ...
    def __ne__(self, arg0: PhotonPipelineResult) -> bool: ...
    def getBestTarget(self) -> PhotonTrackedTarget: 
        """
        Returns the best target in this pipeline result. If there are no targets,
        this method will return an empty target with all values set to zero. The
        best target is determined by the target sort mode in the PhotonVision UI.

        :returns: The best target of the pipeline result.
        """
    def getLatency(self) -> seconds: 
        """
        Returns the latency in the pipeline.

        :returns: The latency in the pipeline.
        """
    def getTargets(self) -> typing.List[PhotonTrackedTarget]: 
        """
        Returns a reference to the vector of targets.

        :returns: A reference to the vector of targets.
        """
    def getTimestamp(self) -> seconds: 
        """
        Returns the estimated time the frame was taken,
        This is much more accurate than using GetLatency()

        :returns: The timestamp in seconds or -1 if this result was not initiated
                  with a timestamp.
        """
    def hasTargets(self) -> bool: 
        """
        Returns whether the pipeline has targets.

        :returns: Whether the pipeline has targets.
        """
    def setTimestamp(self, timestamp: seconds) -> None: 
        """
        Sets the timestamp in seconds

        :param timestamp: The timestamp in seconds
        """
    __hash__ = None
    pass
class PhotonPoseEstimator():
    """
    The PhotonPoseEstimator class filters or combines readings from all the
    fiducials visible at a given timestamp on the field to produce a single robot
    in field pose, using the strategy set below. Example usage can be found in
    our apriltagExample example project.
    """
    def __init__(self, aprilTags: robotpy_apriltag._apriltag.AprilTagFieldLayout, strategy: PoseStrategy, robotToCamera: wpimath.geometry._geometry.Transform3d) -> None: 
        """
        Create a new PhotonPoseEstimator.

        Example: {@code <code>  Map<Integer, Pose3d> map = new HashMap<>();
        map.put(1, new Pose3d(1.0, 2.0, 3.0, new Rotation3d())); // Tag ID 1 is
        at (1.0,2.0,3.0) </code> }

        :param aprilTags:     A AprilTagFieldLayout linking AprilTag IDs to Pose3ds with
                              respect to the FIRST field.
        :param strategy:      The strategy it should use to determine the best pose.
        :param robotToCamera: Transform3d from the center of the robot to the camera
                              mount positions (ie, robot ➔ camera).
        """
    def getFieldLayout(self) -> robotpy_apriltag._apriltag.AprilTagFieldLayout: 
        """
        Get the AprilTagFieldLayout being used by the PositionEstimator.

        :returns: the AprilTagFieldLayout
        """
    def getPoseStrategy(self) -> PoseStrategy: 
        """
        Get the Position Estimation Strategy being used by the Position Estimator.

        :returns: the strategy
        """
    def getReferencePose(self) -> wpimath.geometry._geometry.Pose3d: 
        """
        Return the reference position that is being used by the estimator.

        :returns: the referencePose
        """
    def getRobotToCameraTransform(self) -> wpimath.geometry._geometry.Transform3d: 
        """
        :returns: The current transform from the center of the robot to the camera
                  mount position.
        """
    def setLastPose(self, lastPose: wpimath.geometry._geometry.Pose3d) -> None: 
        """
        Update the stored last pose. Useful for setting the initial estimate when
        using the CLOSEST_TO_LAST_POSE strategy.

        :param lastPose: the lastPose to set
        """
    def setPoseStrategy(self, strat: PoseStrategy) -> None: 
        """
        Set the Position Estimation Strategy used by the Position Estimator.

        :param strategy: the strategy to set
        """
    def setReferencePose(self, referencePose: wpimath.geometry._geometry.Pose3d) -> None: 
        """
        Update the stored reference pose for use when using the
        CLOSEST_TO_REFERENCE_POSE strategy.

        :param referencePose: the referencePose to set
        """
    def setRobotToCameraTransform(self, robotToCamera: wpimath.geometry._geometry.Transform3d) -> None: 
        """
        Useful for pan and tilt mechanisms, or cameras on turrets

        :param robotToCamera: The current transform from the center of the robot to
                              the camera mount position.
        """
    def update(self, result: PhotonPipelineResult) -> typing.Optional[EstimatedRobotPose]: 
        """
        Update the pose estimator.
        """
    pass
class PhotonTrackedTarget():
    """
    Represents a tracked target within a pipeline.
    """
    def __eq__(self, arg0: PhotonTrackedTarget) -> bool: ...
    @typing.overload
    def __init__(self) -> None: 
        """
        Constructs an empty target.

        Constructs a target.

        :param yaw:           The yaw of the target.
        :param pitch:         The pitch of the target.
        :param area:          The area of the target.
        :param skew:          The skew of the target.
        :param pose:          The camera-relative pose of the target.
        :param alternatePose: The alternate camera-relative pose of the target.
                              @Param corners The corners of the bounding rectangle.
        """
    @typing.overload
    def __init__(self, yaw: float, pitch: float, area: float, skew: float, fiducialID: int, pose: wpimath.geometry._geometry.Transform3d, alternatePose: wpimath.geometry._geometry.Transform3d, ambiguity: float, corners: typing.List[typing.Tuple[float, float]], detectedCorners: typing.List[typing.Tuple[float, float]]) -> None: ...
    def __ne__(self, arg0: PhotonTrackedTarget) -> bool: ...
    def getAlternateCameraToTarget(self) -> wpimath.geometry._geometry.Transform3d: 
        """
        Get the transform that maps camera space (X = forward, Y = left, Z = up) to
        object/fiducial tag space (X forward, Y left, Z up) with the highest
        reprojection error
        """
    def getArea(self) -> float: 
        """
        Returns the target area (0-100).

        :returns: The target area.
        """
    def getBestCameraToTarget(self) -> wpimath.geometry._geometry.Transform3d: 
        """
        Get the transform that maps camera space (X = forward, Y = left, Z = up) to
        object/fiducial tag space (X forward, Y left, Z up) with the lowest
        reprojection error. The ratio between this and the alternate target's
        reprojection error is the ambiguity, which is between 0 and 1.

        :returns: The pose of the target relative to the robot.
        """
    def getDetectedCorners(self) -> typing.List[typing.Tuple[float, float]]: 
        """
        Return a list of the n corners in image space (origin top left, x right, y
        down), in no particular order, detected for this target.
        For fiducials, the order is known and is always counter-clock wise around
        the tag, like so

        -> +X     3 ----- 2
        |         |       |
        V + Y     |       |
        0 ----- 1
        """
    def getFiducialId(self) -> int: 
        """
        Get the Fiducial ID of the target currently being tracked,
        or -1 if not set.
        """
    def getMinAreaRectCorners(self) -> typing.List[typing.Tuple[float, float]]: 
        """
        Return a list of the 4 corners in image space (origin top left, x right, y
        down), in no particular order, of the minimum area bounding rectangle of
        this target
        """
    def getPitch(self) -> float: 
        """
        Returns the target pitch (positive-up)

        :returns: The target pitch.
        """
    def getPoseAmbiguity(self) -> float: 
        """
        Get the ratio of pose reprojection errors, called ambiguity. Numbers above
        0.2 are likely to be ambiguous. -1 if invalid.
        """
    def getSkew(self) -> float: 
        """
        Returns the target skew (counter-clockwise positive).

        :returns: The target skew.
        """
    def getYaw(self) -> float: 
        """
        Returns the target yaw (positive-left).

        :returns: The target yaw.
        """
    __hash__ = None
    pass
class PhotonUtils():
    def __init__(self) -> None: ...
    @staticmethod
    def calculateDistanceToTarget(cameraHeight: meters, targetHeight: meters, cameraPitch: radians, targetPitch: radians) -> meters: 
        """
        Algorithm from
        https://docs.limelightvision.io/en/latest/cs_estimating_distance.html
        Estimates range to a target using the target's elevation. This method can
        produce more stable results than SolvePNP when well tuned, if the full 6d
        robot pose is not required.

        :param cameraHeight: The height of the camera off the floor.
        :param targetHeight: The height of the target off the floor.
        :param cameraPitch:  The pitch of the camera from the horizontal plane.
                             Positive valueBytes up.
        :param targetPitch:  The pitch of the target in the camera's lens. Positive
                             values up.

        :returns: The estimated distance to the target.
        """
    @staticmethod
    def estimateCameraToTarget(cameraToTargetTranslation: wpimath.geometry._geometry.Translation2d, fieldToTarget: wpimath.geometry._geometry.Pose2d, gyroAngle: wpimath.geometry._geometry.Rotation2d) -> wpimath.geometry._geometry.Transform2d: 
        """
        Estimates a {@link frc::Transform2d} that maps the camera position to the
        target position, using the robot's gyro. Note that the gyro angle provided
        *must* line up with the field coordinate system -- that is, it should read
        zero degrees when pointed towards the opposing alliance station, and
        increase as the robot rotates CCW.

        :param cameraToTargetTranslation: A Translation2d that encodes the x/y
                                          position of the target relative to the
                                          camera.
        :param fieldToTarget:             A frc::Pose2d representing the target
                                          position in the field coordinate system.
        :param gyroAngle:                 The current robot gyro angle, likely from
                                          odometry.

        :returns: A frc::Transform2d that takes us from the camera to the target.
        """
    @staticmethod
    def estimateCameraToTargetTranslation(targetDistance: meters, yaw: wpimath.geometry._geometry.Rotation2d) -> wpimath.geometry._geometry.Translation2d: 
        """
        Estimate the Translation2d of the target relative to the camera.

        :param targetDistance: The distance to the target.
        :param yaw:            The observed yaw of the target.

        :returns: The target's camera-relative translation.
        """
    @staticmethod
    def estimateFieldToCamera(cameraToTarget: wpimath.geometry._geometry.Transform2d, fieldToTarget: wpimath.geometry._geometry.Pose2d) -> wpimath.geometry._geometry.Pose2d: 
        """
        Estimates the pose of the camera in the field coordinate system, given the
        position of the target relative to the camera, and the target relative to
        the field. This *only* tracks the position of the camera, not the position
        of the robot itself.

        :param cameraToTarget: The position of the target relative to the camera.
        :param fieldToTarget:  The position of the target in the field.

        :returns: The position of the camera in the field.
        """
    @staticmethod
    @typing.overload
    def estimateFieldToRobot(cameraHeight: meters, targetHeight: meters, cameraPitch: radians, targetPitch: radians, targetYaw: wpimath.geometry._geometry.Rotation2d, gyroAngle: wpimath.geometry._geometry.Rotation2d, fieldToTarget: wpimath.geometry._geometry.Pose2d, cameraToRobot: wpimath.geometry._geometry.Transform2d) -> wpimath.geometry._geometry.Pose2d: 
        """
        Estimate the position of the robot in the field.

        :param cameraHeightMeters: The physical height of the camera off the floor
                                   in meters.
        :param targetHeightMeters: The physical height of the target off the floor
                                   in meters. This should be the height of whatever is being targeted (i.e. if
                                   the targeting region is set to top, this should be the height of the top of
                                   the target).
        :param cameraPitchRadians: The pitch of the camera from the horizontal plane
                                   in radians. Positive values up.
        :param targetPitchRadians: The pitch of the target in the camera's lens in
                                   radians. Positive values up.
        :param targetYaw:          The observed yaw of the target. Note that this
                                   *must* be CCW-positive, and Photon returns
                                   CW-positive.
        :param gyroAngle:          The current robot gyro angle, likely from
                                   odometry.
        :param fieldToTarget:      A frc::Pose2d representing the target position in
                                   the field coordinate system.
        :param cameraToRobot:      The position of the robot relative to the camera.
                                   If the camera was mounted 3 inches behind the
                                   "origin" (usually physical center) of the robot,
                                   this would be frc::Transform2d(3 inches, 0
                                   inches, 0 degrees).

        :returns: The position of the robot in the field.

        Estimates the pose of the robot in the field coordinate system, given the
        position of the target relative to the camera, the target relative to the
        field, and the robot relative to the camera.

        :param cameraToTarget: The position of the target relative to the camera.
        :param fieldToTarget:  The position of the target in the field.
        :param cameraToRobot:  The position of the robot relative to the camera. If
                               the camera was mounted 3 inches behind the "origin"
                               (usually physical center) of the robot, this would be
                               frc::Transform2d(3 inches, 0 inches, 0 degrees).

        :returns: The position of the robot in the field.
        """
    @staticmethod
    @typing.overload
    def estimateFieldToRobot(cameraToTarget: wpimath.geometry._geometry.Transform2d, fieldToTarget: wpimath.geometry._geometry.Pose2d, cameraToRobot: wpimath.geometry._geometry.Transform2d) -> wpimath.geometry._geometry.Pose2d: ...
    pass
class PoseStrategy():
    """
    Members:

      LOWEST_AMBIGUITY

      CLOSEST_TO_CAMERA_HEIGHT

      CLOSEST_TO_REFERENCE_POSE

      CLOSEST_TO_LAST_POSE

      AVERAGE_BEST_TARGETS
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    AVERAGE_BEST_TARGETS: photonvision._photonvision.PoseStrategy # value = <PoseStrategy.AVERAGE_BEST_TARGETS: 4>
    CLOSEST_TO_CAMERA_HEIGHT: photonvision._photonvision.PoseStrategy # value = <PoseStrategy.CLOSEST_TO_CAMERA_HEIGHT: 1>
    CLOSEST_TO_LAST_POSE: photonvision._photonvision.PoseStrategy # value = <PoseStrategy.CLOSEST_TO_LAST_POSE: 3>
    CLOSEST_TO_REFERENCE_POSE: photonvision._photonvision.PoseStrategy # value = <PoseStrategy.CLOSEST_TO_REFERENCE_POSE: 2>
    LOWEST_AMBIGUITY: photonvision._photonvision.PoseStrategy # value = <PoseStrategy.LOWEST_AMBIGUITY: 0>
    __members__: dict # value = {'LOWEST_AMBIGUITY': <PoseStrategy.LOWEST_AMBIGUITY: 0>, 'CLOSEST_TO_CAMERA_HEIGHT': <PoseStrategy.CLOSEST_TO_CAMERA_HEIGHT: 1>, 'CLOSEST_TO_REFERENCE_POSE': <PoseStrategy.CLOSEST_TO_REFERENCE_POSE: 2>, 'CLOSEST_TO_LAST_POSE': <PoseStrategy.CLOSEST_TO_LAST_POSE: 3>, 'AVERAGE_BEST_TARGETS': <PoseStrategy.AVERAGE_BEST_TARGETS: 4>}
    pass
class RobotPoseEstimator():
    """
    The RobotPoseEstimator class filters or combines readings from all the
    fiducials visible at a given timestamp on the field to produce a single robot
    in field pose, using the strategy set below. Example usage can be found in
    our apriltagExample example project.
    """
    def __init__(self, aprilTags: robotpy_apriltag._apriltag.AprilTagFieldLayout, strategy: PoseStrategy, cameras: typing.List[typing.Tuple[PhotonCamera, wpimath.geometry._geometry.Transform3d]]) -> None: 
        """
        Create a new RobotPoseEstimator.

        Example: {@code <code>  Map<Integer, Pose3d> map = new HashMap<>();
        map.put(1, new Pose3d(1.0, 2.0, 3.0, new Rotation3d())); // Tag ID 1 is
        at (1.0,2.0,3.0) </code> }

        :param aprilTags: A AprilTagFieldLayout linking AprilTag IDs to Pose3ds with
                          respect to the FIRST field.
        :param strategy:  The strategy it should use to determine the best pose.
        :param cameras:   An ArrayList of Pairs of PhotonCameras and their respective
                          Transform3ds from the center of the robot to the cameras.
        """
    def getFieldLayout(self) -> robotpy_apriltag._apriltag.AprilTagFieldLayout: 
        """
        Get the AprilTagFieldLayout being used by the PositionEstimator.

        :returns: the AprilTagFieldLayout
        """
    def getPoseStrategy(self) -> PoseStrategy: 
        """
        Get the Position Estimation Strategy being used by the Position Estimator.

        :returns: the strategy
        """
    def getReferencePose(self) -> wpimath.geometry._geometry.Pose3d: 
        """
        Return the reference position that is being used by the estimator.

        :returns: the referencePose
        """
    def setCameras(self, cameras: typing.List[typing.Tuple[PhotonCamera, wpimath.geometry._geometry.Transform3d]]) -> None: 
        """
        Set the cameras to be used by the PoseEstimator.

        :param cameras: cameras to set.
        """
    def setLastPose(self, lastPose: wpimath.geometry._geometry.Pose3d) -> None: 
        """
        Update the stored last pose. Useful for setting the initial estimate when
        using the CLOSEST_TO_LAST_POSE strategy.

        :param lastPose: the lastPose to set
        """
    def setPoseStrategy(self, strat: PoseStrategy) -> None: 
        """
        Set the Position Estimation Strategy used by the Position Estimator.

        :param strategy: the strategy to set
        """
    def setReferencePose(self, referencePose: wpimath.geometry._geometry.Pose3d) -> None: 
        """
        Update the stored reference pose for use when using the
        CLOSEST_TO_REFERENCE_POSE strategy.

        :param referencePose: the referencePose to set
        """
    def update(self) -> typing.Tuple[wpimath.geometry._geometry.Pose3d, seconds]: ...
    pass
class SimPhotonCamera(PhotonCamera):
    @typing.overload
    def __init__(self, cameraName: str) -> None: ...
    @typing.overload
    def __init__(self, instance: ntcore._ntcore.NetworkTableInstance, cameraName: str) -> None: ...
    @typing.overload
    def submitProcessedFrame(self, latency: milliseconds, sortMode: typing.Callable[[PhotonTrackedTarget, PhotonTrackedTarget], bool], targetList: typing.List[PhotonTrackedTarget]) -> None: 
        """
        Simulate one processed frame of vision data, putting one result to NT.

        :param latency:    Latency of the provided frame
        :param targetList: List of targets detected

        Simulate one processed frame of vision data, putting one result to NT.

        :param latency:    Latency of the provided frame
        :param sortMode:   Order in which to sort targets
        :param targetList: List of targets detected
        """
    @typing.overload
    def submitProcessedFrame(self, latency: milliseconds, targetList: typing.List[PhotonTrackedTarget]) -> None: ...
    pass
class SimVisionSystem():
    def __init__(self, camName: str, camDiagFOV: degrees, cameraToRobot: wpimath.geometry._geometry.Transform3d, maxLEDRange: meters, cameraResWidth: int, cameraResHeight: int, minTargetArea: float) -> None: 
        """
        Create a simulated vision system involving a camera and coprocessor mounted
        on a mobile robot running PhotonVision, detecting one or more targets
        scattered around the field. This assumes a fairly simple and
        distortion-less pinhole camera model.

        :param camName:         Name of the PhotonVision camera to create. Align it with the
                                settings you use in the PhotonVision GUI.
        :param camDiagFOV:      Diagonal Field of View of the camera used. Align it with
                                the manufacturer specifications, and/or whatever is configured in the
                                PhotonVision Setting page.
        :param cameraToRobot:   Transform to move from the camera's mount position to
                                the robot's position
        :param maxLEDRange:     Maximum distance at which your camera can illuminate the
                                target and make it visible. Set to 9000 or more if your vision system does
                                not rely on LED's.
        :param cameraResWidth:  Width of your camera's image sensor in pixels
        :param cameraResHeight: Height of your camera's image sensor in pixels
        :param minTargetArea:   Minimum area that that the target should be before
                                it's recognized as a target by the camera. Match this with your contour
                                filtering settings in the PhotonVision GUI.
        """
    def addSimVisionTarget(self, target: SimVisionTarget) -> None: 
        """
        Add a target on the field which your vision system is designed to detect.
        The PhotonCamera from this system will report the location of the robot
        relative to the subset of these targets which are visible from the given
        robot position.

        :param target: Target to add to the simulated field
        """
    def camCamSeeTarget(self, dist: meters, yaw: radians, pitch: radians, area: float) -> bool: ...
    def clearVisionTargets(self) -> None: 
        """
        Clears all sim vision targets.
        This is useful for switching alliances and needing to repopulate the sim
        targets. NOTE: Old targets will still show on the Field2d unless
        overwritten by new targets with the same ID
        """
    def getM2PerPx(self, dist: meters) -> square_meters: ...
    def moveCamera(self, newCameraToRobot: wpimath.geometry._geometry.Transform3d) -> None: 
        """
        Adjust the camera position relative to the robot. Use this if your camera
        is on a gimbal or turret or some other mobile platform.

        :param newCameraToRobot: New Transform from the robot to the camera
        """
    @typing.overload
    def processFrame(self, robotPose: wpimath.geometry._geometry.Pose2d) -> None: 
        """
        Periodic update. Call this once per frame of image data you wish to process
        and send to NetworkTables

        :param robotPose: current pose of the robot on the field. Will be used to
                          calculate which targets are actually in view, where they are at relative to
                          the robot, and relevant PhotonVision parameters.

        Periodic update. Call this once per frame of image data you wish to process
        and send to NetworkTables

        :param robotPose: current pose of the robot in space. Will be used to
                          calculate which targets are actually in view, where they are at relative to
                          the robot, and relevant PhotonVision parameters.
        """
    @typing.overload
    def processFrame(self, robotPose: wpimath.geometry._geometry.Pose3d) -> None: ...
    @property
    def cam(self) -> SimPhotonCamera:
        """
        :type: SimPhotonCamera
        """
    @property
    def cameraToRobot(self) -> wpimath.geometry._geometry.Transform3d:
        """
        :type: wpimath.geometry._geometry.Transform3d
        """
    @property
    def dbgCamera(self) -> wpilib._wpilib.FieldObject2d:
        """
        :type: wpilib._wpilib.FieldObject2d
        """
    @property
    def dbgField(self) -> wpilib._wpilib.Field2d:
        """
        :type: wpilib._wpilib.Field2d
        """
    @property
    def dbgRobot(self) -> wpilib._wpilib.FieldObject2d:
        """
        :type: wpilib._wpilib.FieldObject2d
        """
    @property
    def targetList(self) -> typing.List[SimVisionTarget]:
        """
        :type: typing.List[SimVisionTarget]
        """
    pass
class SimVisionTarget():
    def __init__(self, targetPose: wpimath.geometry._geometry.Pose3d, targetWidth: meters, targetHeight: meters, targetId: int) -> None: 
        """
        Describes a vision target located somewhere on the field that your
        SimVisionSystem can detect.

        :param targetPose:   Pose3d of the target in field-relative coordinates
        :param targetWidth:  Width of the outer bounding box of the target.
        :param targetHeight: Pair Height of the outer bounding box of the
                             target.
        :param targetId:     Id of the target
        """
    @property
    def targetArea(self) -> square_meters:
        """
        :type: square_meters
        """
    @property
    def targetHeight(self) -> meters:
        """
        :type: meters
        """
    @property
    def targetId(self) -> int:
        """
        :type: int
        """
    @targetId.setter
    def targetId(self, arg0: int) -> None:
        pass
    @property
    def targetPose(self) -> wpimath.geometry._geometry.Pose3d:
        """
        :type: wpimath.geometry._geometry.Pose3d
        """
    @property
    def targetWidth(self) -> meters:
        """
        :type: meters
        """
    pass
