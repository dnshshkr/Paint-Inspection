/*
    Note: Before getting started, Basler recommends reading the Programmer's Guide topic
    in the pylon .NET API documentation that gets installed with pylon.

    This sample shows how to use the Exposure End event to speed up image acquisition.
    For example, when a sensor exposure is finished, the camera can send an Exposure End event to the computer.
    The computer can receive the event before the image data of the finished exposure has been transferred completely.
    This avoids unnecessary delays, e.g., when an image object moves before the related image data transfer is complete.

    Note: This sample shows how to match incoming images using the PLCamera.EventExposureEndFrameID and the GrabResult.BlockID values. For ace 2 camera models, PLCamera.EventExposureEndFrameID and the GrabResult.BlockID don't contain matching values. The GrabResult.BlockID equivalent is the chunk value represented by PLCamera.ChunkSelector.FrameID. Please see the Grab_ChunkImage sample for more information about how to determine the correct chunk value to use instead of GrabResult.BlockID.
*/

using System;
using System.Collections.Generic;
using Basler.Pylon;
using System.Diagnostics;

namespace Grab_UsingExposureEndEvent
{
    // Used for logging received events without outputting the information on the screen
    // because outputting will change the timing.
    // This class is used for demonstration purposes only.
    internal class LogItem
    {
        private string eventType;
        private long frameNumber;
        private double time;

        public string EventType
        {
            get
            {
                return this.eventType;
            }
        }
        public long FrameNumber
        {
            get
            {
                return this.frameNumber;
            }
        }
        public double Time
        {
            get
            {
                return time;
            }
        }

        //Stores the values inside private variables.
        public LogItem( string type, long frameNr )
        {
            eventType = type;
            frameNumber = frameNr;
            time = Stopwatch.GetTimestamp();
        }
    };

    class Grab_UsingExposureEndEvent
    {
        private static Version sfnc2_0_0 = new Version(2, 0, 0);

        private static long nextExpectedFrameNumberImage;
        private static long nextExpectedFrameNumberExposureEnd;
        private static long nextFrameNumberForMove;
        private static bool gevCounterRules;

        private static string eventNotificationOn;
        private static IntegerName exposureEndEventFrameId;

        // Number of images to be grabbed.
        public static long countOfImagesToGrab = 50;
        // Create list of log items.
        public static List<LogItem> logItems = new List<LogItem>();


        private static void Configure( Camera camera )
        {
            // Camera event processing must be enabled first. The default is off.
            // The camera must be closed to do this.
            if (camera.Parameters[PLCameraInstance.GrabCameraEvents].IsWritable)
            {
                camera.Parameters[PLCameraInstance.GrabCameraEvents].SetValue( true );
            }
            else
            {
                throw new Exception( "Can't enable GrabCameraEvents." );
            }

            // Open the camera to configure parameters.
            camera.Open();

            // Check whether the device supports events.
            if (!camera.Parameters[PLCamera.EventSelector].IsWritable)
            {
                throw new Exception( "The device doesn't support events." );
            }

            // GigE cameras don't use frame ID 0.
            gevCounterRules = camera.CameraInfo[CameraInfoKey.TLType] == TLType.GigE;

            if (camera.GetSfncVersion() < sfnc2_0_0)
            {
                // On older cameras, frame IDs start at 1.
                nextExpectedFrameNumberImage = 1;
                nextExpectedFrameNumberExposureEnd = 1;
                nextFrameNumberForMove = 1;

                // The naming of the Exposure End event differs between SFNC 2.0 and previous versions.
                exposureEndEventFrameId = PLCamera.ExposureEndEventFrameID;
                eventNotificationOn = PLCamera.EventNotification.GenICamEvent;

                // Add an event handler that notifies you when an Exposure End event is received.
                // On older cameras, the parameter is called "ExposureEndEventData".
                camera.Parameters["ExposureEndEventData"].ParameterChanged += delegate ( Object sender, ParameterChangedEventArgs e )
                {
                    OnCameraEventExposureEndData( sender, e, camera );
                };
            }
            else
            {
                // On current cameras (using SFNC 2.0, e.g., USB3 Vision cameras),
                // frame IDs start at 0.
                nextExpectedFrameNumberImage = 0;
                nextExpectedFrameNumberExposureEnd = 0;
                nextFrameNumberForMove = 0;

                // The naming of the Exposure End event differs between SFNC 2.0 and previous versions.
                exposureEndEventFrameId = PLCamera.EventExposureEndFrameID;
                eventNotificationOn = PLCamera.EventNotification.On;

                // Add an event handler that notifies you when an Exposure End event is received.
                // On current cameras, the parameter is called "EventExposureEndData".
                camera.Parameters["EventExposureEndData"].ParameterChanged += delegate ( Object sender, ParameterChangedEventArgs e )
                {
                    OnCameraEventExposureEndData( sender, e, camera );
                };

            }

            // Event handler for images received.
            camera.StreamGrabber.ImageGrabbed += OnImageGrabbed;

            // The network packet signaling an event on a GigE camera device may get lost in the network.
            // The following commented parameters can be used to control the handling of lost events.
            //camera.Parameters[ParametersPLGigEEventGrabber.Timeout]
            //camera.Parameters[PLGigEEventGrabber.RetryCount]

            // Enable the sending of Exposure End events.
            // Select the event to be received.
            camera.Parameters[PLCamera.EventSelector].SetValue( PLCamera.EventSelector.ExposureEnd );
            camera.Parameters[PLCamera.EventNotification].SetValue( eventNotificationOn );
        }


        private static void Disable( Camera camera )
        {
            // Disable the sending of Exposure End events.
            camera.Parameters[PLCamera.EventSelector].SetValue( PLCamera.EventSelector.ExposureEnd );
            camera.Parameters[PLCamera.EventNotification].SetValue( PLCamera.EventNotification.Off );
        }


        private static long GetIncrementedFrameNumber( long frameNr )
        {
            frameNr++;

            // GigE cameras use a 16 bit value and will wrap around earlier.
            // They skip the value of 0 and continue with 1
            if (gevCounterRules && unchecked((UInt16)frameNr) == 0)
            {
                frameNr = 1;
            }

            return frameNr;
        }


        private static void MoveImagedItemOrSensorHead()
        {
            // The imaged item or the sensor head can be moved now...
            // The camera may not be ready yet for a trigger at this point because the sensor is still being read out.
            // See the documentation of the CInstantCamera::WaitForFrameTriggerReady() method for more information.
            logItems.Add( new LogItem( "Move", nextFrameNumberForMove ) );
            nextFrameNumberForMove = GetIncrementedFrameNumber( nextFrameNumberForMove );
        }


        private static void OnCameraEventExposureEndData( Object sender, ParameterChangedEventArgs e, Camera camera )
        {
            // An image has been received. The block ID is equal to the frame number on GigE camera devices.
            long frameNumber = 0;
            if (camera.Parameters[exposureEndEventFrameId].IsReadable)
            {
                frameNumber = camera.Parameters[exposureEndEventFrameId].GetValue();
            }
            logItems.Add( new LogItem( "ExposureEndEvent", frameNumber ) );

            if (GetIncrementedFrameNumber( frameNumber ) != nextExpectedFrameNumberExposureEnd)
            {
                // Check whether the imaged item or the sensor head can be moved.
                // This will be the case if the Exposure End event has been lost or if the Exposure End event is received later than the image.
                if (frameNumber == nextFrameNumberForMove)
                {
                    MoveImagedItemOrSensorHead();
                }

                // Check for missing events.
                if (frameNumber != nextExpectedFrameNumberExposureEnd)
                {
                    logItems.Add( new LogItem( "An Exposure End event has been lost. Expected frame number is " + nextExpectedFrameNumberExposureEnd + " but got frame number " + frameNumber, frameNumber ) );
                    // Resync.
                    nextExpectedFrameNumberExposureEnd = frameNumber;
                }

                nextExpectedFrameNumberExposureEnd = GetIncrementedFrameNumber( nextExpectedFrameNumberExposureEnd );
            }
        }


        // This handler is called when an image has been received.
        private static void OnImageGrabbed( Object sender, ImageGrabbedEventArgs e )
        {
            // Read frame number from grab result.
            long frameNumber = e.GrabResult.BlockID;
            logItems.Add( new LogItem( "Image Received", frameNumber ) );

            if (frameNumber == nextFrameNumberForMove)
            {
                MoveImagedItemOrSensorHead();
            }

            // Check for missing images.
            if (frameNumber != nextExpectedFrameNumberImage)
            {
                logItems.Add( new LogItem( "An image has been lost. Expected frame number is " + nextExpectedFrameNumberExposureEnd + " but got frame number " + frameNumber, frameNumber ) );
                // Resync.
                nextExpectedFrameNumberImage = frameNumber;
            }

            nextExpectedFrameNumberImage = GetIncrementedFrameNumber( nextExpectedFrameNumberImage );
        }

        // This will print all the log items to console.
        private static void PrintLog()
        {
            Console.WriteLine( "Warning. The time values printed may not be correct on older computer hardware." );
            Console.WriteLine( "Time [ms]    Event                 Frame Number" );
            Console.WriteLine( "----------   ----------------      --------------" );
            
            var ticks = new List<double>();
            
            foreach (LogItem item in logItems)
            {
                ticks.Add( item.Time );
            }

            int i = 0;
            foreach (LogItem item in logItems)
            {
                double time_ms = 0;
                if (i > 0)
                {
                    double newTicks = ticks[i];
                    double oldTicks = ticks[i - 1];
                    time_ms = (((newTicks - oldTicks)) * 1000 / Stopwatch.Frequency);
                }
                
                i++;
                
                // {0,10:0.0000} Formatting the size of time_ms to 10 spaces and precision of 4.
                Console.WriteLine( String.Format( "{0,10:0.0000}", time_ms ) + " {0,18}       {1}", item.EventType, item.FrameNumber );
            }
        }

        internal static void Main()
        {
            // The exit code of the sample application.
            int exitCode = 0;
            try
            {
                // Create a camera object that selects the first camera device found.
                // More constructors are available for selecting a specific camera device.
                using (Camera camera = new Camera())
                {
                    // Print the model name of the camera.
                    Console.WriteLine( "Using camera {0}.", camera.CameraInfo[CameraInfoKey.ModelName] );
                    if (camera.CameraInfo[CameraInfoKey.ModelName].StartsWith( "a2A" ))
                    {
                        Console.WriteLine( "Note: This sample may not work as expected when used with ace 2 cameras." );
                        Console.WriteLine( "      Please see note at the beginnging of the sample for details." );
                    }

                    // Configure the camera.
                    Configure( camera );

                    // Start grabbing of countOfImagesToGrab images.
                    // The camera device is operated in a default configuration that
                    // sets up free-running continuous acquisition.
                    camera.StreamGrabber.Start( countOfImagesToGrab );

                    IGrabResult result;
                    while (camera.StreamGrabber.IsGrabbing)
                    {
                        // Retrieve grab results and notify the camera event and image event handlers.
                        result = camera.StreamGrabber.RetrieveResult( 5000, TimeoutHandling.ThrowException );
                        using (result)
                        {
                            // Nothing to do here with the grab result. The grab results are handled by the registered event handlers.
                        }
                    }

                    // Disable events.
                    Disable( camera );

                    // Print the recorded log showing the timing of events and images.
                    PrintLog();

                    // Close the camera.
                    camera.Close();
                }
            }
            catch (Exception e)
            {
                // Error handling.
                Console.Error.WriteLine( "Exception: {0}", e.Message );
                exitCode = 1;
            }
            finally
            {
                // Comment the following two lines to disable waiting on exit.
                Console.Error.WriteLine( "\nPress enter to exit." );
                Console.ReadLine();
            }

            Environment.Exit( exitCode );
        }
    }
}
