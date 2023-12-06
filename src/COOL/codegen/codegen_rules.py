
PUSH_STACK=\
"""    # Push stack
    addiu $sp, $sp, -4
    sw ${register}, 0($sp)
"""


POP_STACK=\
"""    # Pop stack
    lw ${register}, 0($sp)
    addiu $sp, $sp, 4
"""


CREATE_CLASS=\
"""
# Create class {class_name}
{class_name}:
{request_memory}

{attributes}
"""


CREATE_FUNCTION=\
"""
# Create function {function_name} from class {class_name}
{function_name}:
    addiu $sp, $sp, -4
    sw $ra, 0($sp)
{method}
{clean_stack}
    lw $ra, 0($sp)
    addiu $sp, $sp, 4
    jr $ra
"""
