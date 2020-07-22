# Decoding H.264 with Android API
This sample is about decoding h264 flux with Android API.

## H.264 flux
The h264 data consist of a multitude of NAL Unit (NALU). Each NAL Unit contains either meta-data relative to the h264 format, either partial frame or a full picture.
These NAL Unit can be streamed through the RTP protocol, but it is not our topic.

In our case the h264 data is writted in a file or streamed throug the TCP/IP protocol. In the two cases the NAL Unit can be retreived because they start with a `0x00 0x00 0x00 0x01` or `0x00 0x00 0x01` sequence (depending on the encoder).

## Android MediaCodec
In the Android part we must do three things:
- Add a [`SurfaceView`](https://developer.android.com/reference/android/view/SurfaceView) to our layout.
- Implements [`SurfaceHolder.Callback`](https://developer.android.com/reference/android/view/SurfaceHolder.Callback) to handle some event.
- Instantiate a [`Mediacodec`](https://developer.android.com/reference/android/media/MediaCodec) object, and feed it with NAL Unit (**whitout** the `0x00 0x00 0x00 0x01` sequence).

The Mediacodec work like this: You have two things to do in parallel. One is request for empty buffer and fill it, secondly is waiting for decoded frames and trigger its render. These two part uses blocking function, so you must use thread (runnable, asynkTask or assimillable).

### More about the MediaCodec
I use [`createDecoderByType(String type)`](https://developer.android.com/reference/android/media/MediaCodec#createDecoderByType(java.lang.String)) to instatiate the MediaCodec. Is not the best way, see the note in Android documentation. Then `configure (MediaFormat format, Surface surface, int flags, MediaDescrambler descrambler)` the MediaCodec, passing it a MediaFormat created with `createVideoFormat (String mime, int width, int height)` (where `mime` can be `"video/avc"`), a `SurfaceView` and the rest can be `null`

You have to `start()` the MediaCodec and fill their buffers's using `dequeueInputBuffer (long timeoutUs)` to obtain the ID/index of a free buffer and get the instance using `getInputBuffer (int index)`\*.\
When the buffer is filled with the NAL Unit (**whitout** the `0x00 0x00 0x00 0x01` sequence) you can `queueInputBuffer (int index, int offset, int size, long presentationTimeUs, int flags)`\*\* for the MediaCodec proceed it.\
Because `dequeueInputBuffer (long timeoutUs)` is blocking you must do this in a separate thread.\
\**(in older api you must `getInputBuffers()` (the array of buffers) `dequeueInputBuffer (long timeoutUs)` and `clear()` it before writting)*\
\*\**(in our case the parameter `long presentationTimeUs` is not used, this information is find by the MediaCodec in a NAL Unit, set it to `-1`, and flags is not used too, set it to `0`)*

In parallel you have to `dequeueOutputBuffer (MediaCodec.BufferInfo info, long timeoutUs)`. These function is bloking and return an `int` which can be a sepcial value (see the doc) indicate some stats of the Mediacodec (like the numbers of outBuffers has changed, but it not be used in our case) or an index of a buffer ready to be automatically rendered to the `SurfaceView` by call to `releaseOutputBuffer (int index, boolean render)`.\
Because `dequeueOutputBuffer (MediaCodec.BufferInfo info, long timeoutUs)` is blocking you must do this in a separate thread.

Don't forget to `stop()` and `release()` the MediaCodec.

## The Client
I propose a basic Python script who send the sample as client. Yon can send the entire file directly in one time or by aleatory sized part or "manually" using the Python shell.

## The Sample
The h264 sample is recorded from a Raspberry with the [picamera lib](https://picamera.readthedocs.io/en/release-1.13/)

## See
https://yumichan.net/video-processing/video-compression/introduction-to-h264-nal-unit/
https://en.wikipedia.org/wiki/Network_Abstraction_Layer
