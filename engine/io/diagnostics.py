print_clear = lambda s: print(s, end="")

def write_display(dataDict):
    print_clear("\u001b[1000D")
    print_clear("\u001b[8A")
    print_clear("Diagnostic Display... \n \n"
          "ADC Value:                       %(adc_value)f \n"
          "Serve Button State:              %(serve_button_state)r \n"
          "Super Bat Button State:          %(super_button_state)r \n"
          "Bat Position:                 x: %(bat_left_pos_x)f  y: %(bat_left_pos_y)f \n"
          "Bat Position:                 x: %(bat_right_pos_x)f  y: %(bat_right_pos_y)f \n"
          "Ball Position:                x: %(ball_pos_x)f  y: %(ball_pos_y)f \n" % dataDict)
