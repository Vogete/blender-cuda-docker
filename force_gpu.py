import bpy, _cycles
for card in bpy.context.user_preferences.addons['cycles'].preferences.devices:
    print(card.name)

prefs = bpy.context.user_preferences.addons['cycles'].preferences
prefs.compute_device_type = 'CUDA'
prefs.devices[0].use = True

bpy.ops.wm.save_userpref()
