program teste4; 
var flag: boolean;
var cont, input: integer;
var x, y, z: real;
var teste: string;
begin 
	cont := 0;
	flag := true; 
	x := 3.7;
	y:= 0.45;      
	teste := "Estou aqui"; 
	print x / y;   
	read input; 
	while flag do 
		cont := cont + 1;
		if cont == 5 then
			z := x - y;
			z := z/10 + 4 - 3;
		end 
		if cont != 10 
			then flag := false; 
		end             
	end 
end 