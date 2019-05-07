# Slic3r - Gcode Heat tower manipulator
 
Small script that manipulate the gcode for heat tower print.
I recommend to follow this documentation for preparing your slice:

https://github.com/slic3r/Slic3r/wiki/Calibration-of-Slic3r

You need to add this line in "After layer change G-Code":

```python
; Layer [layer_num]
```

STL: https://www.thingiverse.com/thing:1548697

Doc: <https://github.com/slic3r/Slic3r/wiki/Calibration-of-Slic3r>

Misc:
If minimum temperature is reached all following layer will stay there. 

If output file exists, it will be removed. 



If there are problems, please tell me!

No warranty!! 
