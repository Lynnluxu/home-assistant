action = data.get("action")
brightness = float(data.get("brightness"))
target_id = data.get("target_id")

# There's too much latency to implement smooth "*-hold" and "*-hold-release"
# features.
if "hold" in action:
  raise NotImplementedError


def next_white_temperature(target_id, length=4):
  assert length >= 2

  target_state = hass.states.get(target_id)

  lower = target_state.attributes['min_mireds']
  upper = target_state.attributes['max_mireds']
  candidates = [lower + x * (upper - lower) // (length - 1)
                for x in range(length)]

  current = target_state.attributes['color_temp']

  # Find next greater temperature, or cycle otherwise
  for new in candidates:
    if new > current:
      break
  else:
    new = candidates[0]

  return new


service = "turn_off" if action.startswith("off") else "turn_on"

service_data = {"entity_id": target_id, "transition": 1}
if service != "turn_off":
  service_data["brightness"] = brightness
if action == "on-press" and hass.states.get(target_id).state == "on":
  # Cycle through white temperatures
  # XXX: this does not work well with concurrent calls
  service_data["color_temp"] = next_white_temperature(target_id, 5)

hass.services.call("light", service, service_data)
