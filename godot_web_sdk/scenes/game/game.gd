extends Control

const COUNTRY_CODE: = "7"
@onready var game_scene = preload("res://scenes/game/game.tscn")
var sip_login:= "<your_sip_login>"
var sip_password:= "<your_sip_password>"
var window
var correct_phone

func fload():
	var file = FileAccess.open("res://game-config.json", FileAccess.READ)
	var content = file.get_as_text()
	file.close()
	var result_json = JSON.parse_string(content)
	return result_json

func string_to_array_pairs(text: String) -> Array:
	var result = []
	for i in range(0, text.length() - (text.length() % 2), 2): # Adjust range to avoid odd last char
		result.append(text.substr(i, 2))
	return result

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	Events.connect("pannel_change_number",on_pannel_change_number)
	var user_config = fload()
	correct_phone = user_config["phone"]
	var phone_array = string_to_array_pairs(correct_phone)
	
	# fill number containers
	var number_containers = [%NP1,%NP2,%NP3,%NP4,%NP5]
	for i in number_containers.size():
		number_containers[i].change_correct_number(phone_array[i])
	
	# shuffle for random fill numbers
	phone_array.shuffle()
	var nodes :=get_tree().get_nodes_in_group("Numbers")
	for i in nodes.size():
		nodes[i].change_current_number(phone_array[i])


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func get_numbers(numbers:Array) -> String:
	var text:= ""
	for n in numbers:
		text += n.current_number
	return text

func _on_button_pressed() -> void:
	# get phone number to call
	var np_array := [%NP1,%NP2,%NP3,%NP4,%NP5]
	var phone := get_numbers(np_array)
	# make phone call via SIP connection
	window.sip_instance.call(COUNTRY_CODE+phone)


func on_pannel_change_number():
	var np_array := [%NP1,%NP2,%NP3,%NP4,%NP5]
	var phone := get_numbers(np_array)
	
	if phone == correct_phone:
		# create SIP connection in JS window object 
		%CallButton.text = "Позвонить на номер +{0}{1}".format([COUNTRY_CODE,phone])
		JavaScriptBridge.eval("window.sip_instance=WebVoiceSdk.createSipInstance({
		  sipLogin: '{0}',
		  sipPassword: '{1}',
		})".format([sip_login,sip_password]),true)
		# register SIP connection
		JavaScriptBridge.eval("window.sip_instance.register()",true)
		# git JS window object as godot object
		window = JavaScriptBridge.get_interface("window")
		if (window):
			%CallButton.disabled = false
		else:
			push_error("Works only in browser")
			%CallButton.text = "Чтобы сделать вызов откройте игру в браузере"

# instance new game scene for reset
func _on_new_game_pressed() -> void:
	get_tree().change_scene_to_packed(game_scene)
