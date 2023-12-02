class Main inherits IO {
	-- the class has features. Only methods in this case.
	x: Int;
	main(): Object {
		{
			out_string("Enter n to find nth fibonacci number!\n");
			x <- in_int();
			out_int(x);
			out_string("\n");
			x <- x + x;
			out_int(x);
			
			out_string("\n");
			
		}
	};

	fib(i : Int) : Int {	
			{
				out_int(i);
				1;
			}
			
	};

};
