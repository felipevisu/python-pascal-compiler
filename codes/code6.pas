program teste6; 
var count, input: integer;
var x: real;
begin 
	x := 3.7;    
	for count := 0 to 10 do
		read input;
		x := x + input;
	write x;
end 