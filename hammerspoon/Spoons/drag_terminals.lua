
local rectanglePreviewColor = '#81ecec'
local rectanglePreview = hs.drawing.rectangle(
    hs.geometry.rect(0, 0, 0, 0)
)

rectanglePreview:setStrokeWidth(2)
rectanglePreview:setStrokeColor({ hex=rectanglePreviewColor, alpha=1 })
rectanglePreview:setFillColor({ hex=rectanglePreviewColor, alpha=0.5 })
rectanglePreview:setRoundedRectRadii(2, 2)
rectanglePreview:setStroke(true):setFill(true)
rectanglePreview:setLevel('floating')

local function openIterm()
    local frame = rectanglePreview:frame()
    local createItermWithBounds = string.format([[
    if application "iTerm" is not running then 
        activate application "iTerm"
    end if
    tell application "iTerm"
        set newWindow to (create window with default profile)
        set the bounds of newWindow to {%i, %i, %i, %i}
    end tell
    ]], frame.x, frame.y, frame.x + frame.w, frame.y + frame.h)
    hs.osascript.applescript(createItermWithBounds)
end

local fromPoint = nil

local drag_event = hs.eventtap.new(
    { hs.eventtap.event.types.mouseMoved },
    function(e)
        toPoint = hs.mouse.getAbsolutePosition()
        local newFrame = hs.geometry.new({
            ["x1"] = fromPoint.x, 
            ["y1"] = fromPoint.y, 
            ["x2"] = toPoint.x, 
            ["y2"] = toPoint.y, 
        })
        rectanglePreview:setFrame(newFrame)

        return nil
    end
)

local flags_event = hs.eventtap.new(
    { hs.eventtap.event.types.flagsChanged },
    function(e)
        local flags = e:getFlags()
        if flags.ctrl and flags.shift then
            fromPoint = hs.mouse.getAbsolutePosition()
            local newFrame = hs.geometry.rect(fromPoint.x, fromPoint.y, 0, 0)
            rectanglePreview:setFrame(newFrame)
            drag_event:start()
            rectanglePreview:show()
        elseif fromPoint ~= nil then
            fromPoint = nil
            drag_event:stop()
            rectanglePreview:hide()
            openIterm()
        end

        return nil

    end
)

flags_event:start()












