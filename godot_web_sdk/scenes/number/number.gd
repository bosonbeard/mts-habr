extends Control



@export var currentNumber := "00"
var drag_preview
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	$Panel/NumberLabel.text =  currentNumber

func change_color(hexcolor:String):
	$Panel/NumberLabel.set("theme_override_colors/font_color",hexcolor)

func change_current_number(number:String):
	currentNumber = number
	$Panel/NumberLabel.text =  currentNumber


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
	
func _get_drag_data(at_position: Vector2):
	var preview = load('res://scenes/number/number.tscn').instantiate()
	set_drag_preview(preview)
	preview.change_current_number(currentNumber)
	drag_preview = preview
	return self
