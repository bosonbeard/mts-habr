extends Control

@export var correct_number := "00"
@export var current_number = "--"


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.

# change container number
func change_current_number(number:String):
	current_number = number
	$Panel/NumberLabel.text =  current_number
	
func change_correct_number(number:String):
	correct_number = number

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func _can_drop_data(at_position: Vector2, data: Variant):
	
	# color hint for drag and drop
	if data.currentNumber == self.correct_number:
		data.drag_preview.change_color("#00FF00")
		return true
	else:
		data.drag_preview.change_color("#FF0000")
		return false
	
func _drop_data(at_position: Vector2, data: Variant):
	# change number in receiver container and delete dropped panel
	change_current_number (data.currentNumber)
	data.queue_free()
	Events.pannel_change_number.emit()
