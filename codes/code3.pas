program prog2; 
var flag: boolean;
var cont: integer;
begin 
	cont := 0;
	flag := true; 
	while flag do 
		cont := cont + 1;
		if cont > 10 
			then flag := false; 
		end 
	end 
end
