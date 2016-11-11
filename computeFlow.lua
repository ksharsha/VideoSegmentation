local cv = require 'cv'
require 'cv.highgui'
require 'cv.videoio'
require 'cv.imgproc'

local cap = cv.VideoCapture{config.vid}
if not cap:isOpened() then
    print("Failed to open the specified video")
    os.exit(-1)
end

local videoWriter = cv.VideoWriter{
   "outFlow.mp4",
   cv.VideoWriter.fourcc{'D', 'I', 'V', 'X'}, -- or any other codec
   fps = 25,
   frameSize = frameToSaveSize
}

if not videoWriter:isOpened() then
   print('Failed to initialize video writer. Possibly wrong codec or file name/path trouble')
   os.exit(-1)
end

local _, prev = cap:read{};
-- local flowFrames = {};
-- local c = 0;
while cap:isOpened() do
    local _, frame = cap:read{};
    -- compute optical flow between prev frame and current frame
    local flow = cv.calcOpticalFlowFarneback(prev, frame, nil, 0.5, 3, 15, 3, 5, 1.2, 0);
    local mag, ang = cv.cartToPolar(flow[{{},0}], flow[{{},1}])
    hsv[{{},0}] = ang*180/math.pi/2
    hsv[{{}, 2}] = cv.normalize(mag, nil, 0, 255, cv.NORM_MINMAX)
    bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)

    videoWriter:write{bgr};
    -- flowFrames[c] = bgr;
    -- c = c + 1;
end

