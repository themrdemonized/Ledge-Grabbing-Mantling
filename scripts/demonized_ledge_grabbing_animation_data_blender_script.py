# Python script for export anim data in blender
# Paste in Blender scripting window
# exported camera_root

import bpy

context = bpy.context
obj = context.object
action =  context.object.animation_data.action
print(context)
print(obj)
print(action)
indexToAxis = {
    0: 'X',
    1: 'Z',
    2: 'Y',
    3: 'Y',
    4: 'Z',
    5: 'X'
}

length = context.scene.frame_end
fps = context.scene.render.fps
animTime = length / fps 
curves = {}
j = 0
for fcurve in action.fcurves:
    i = 0
    time = 0
    curve = {}
    p1 = None
    p2 = None
    p3 = None
    p4 = None
    for kfp in fcurve.keyframe_points:
        # Get control point
        p1 = [kfp.co[0], kfp.co[1]]
        
        # Get right handle
        p2 = [kfp.handle_right[0], kfp.handle_right[1]]
        
        # Get next control point left handle
        nextIndex = i + 1
        nextKfp = None
        if nextIndex < len(fcurve.keyframe_points):
            nextKfp = fcurve.keyframe_points[nextIndex]
            p3 = [nextKfp.handle_left[0], nextKfp.handle_left[1]]
        
            # Get next control point
            p4 = [nextKfp.co[0], nextKfp.co[1]]
        else:
            p1 = [kfp.co[0], kfp.co[1]]
            p2 = [length, kfp.co[1]]
            p3 = [length, kfp.co[1]]
            p4 = [length, kfp.co[1]]
        curve[p1[0] / fps] = [p1, p2, p3, p4]
        i = i + 1
    curve[animTime] = [p4, p4, p4, p4]
    curves[fcurve.data_path + indexToAxis[j]] = curve
    j = j + 1

formattedCurves = ""
for curve in curves:
    s = f"{curve} = {{"
    for time in curves[curve]:
        data = curves[curve][time]
        s += "\n\t\t[%s] = %s" % (time, f"{{ vector():set({data[0][0]}, {data[0][1]}, 0), vector():set({data[1][0]}, {data[1][1]}, 0), vector():set({data[2][0]}, {data[2][1]}, 0), vector():set({data[3][0]}, {data[3][1]}, 0), }},")
    formattedCurves += s + "\n\t},\n\t"
print(f"""
data = {{
    animationFrameLength = {length},
    originalFps = {fps},
    calculatedTime = {animTime},

    -- Below is the data to modify manually
    -- Modifier to camera rotations
    rotationModifier = 1,

    -- Frame starting from prebaked animation will be used fully
    animInFrame = 26,

    -- Frame from which prebaked animation will blend out to procedural animation
    animOutFrame = 50,

    -- Speed of animation
    animationSpeed = 1,

    -- Speed of hands animation, affected by overall animationSpeed
    hudMotionSpeed = 1,

    -- Frame to play grunt sound
    gruntSoundFrame = 26,

    -- Generated curves, touch with care
    curves = {{
        {formattedCurves}      
    }}
}}    
""") 
