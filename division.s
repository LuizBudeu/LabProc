;@ r0 - Divisor
;@ r1 - Dividendo
;@ r2 - Resto
;@ r3 - Resultado
;@ r4 - Contador de shifts
_divide:
	cmp r0, #0
	beq _end_divisao    ;@ Retorna se divisor for zero
	mov r3, #0          ;@ Zera quosciente
	mov r2, #0          ;@ Zera parcela
	clz r4, r1          ;@ r4 recebe o número de zeros a esquerda do dividendo e será o ocntador de deslocamento
	movs r1, r1, lsl r4 ;@ Desloca dividendo para remover zeros a esquerda
_desloca:
	cmp r4, #32
	beq _end_divisao
	mov r2, r2, lsl #1  ;@ Desloca parcela
	mov r3, r3, lsl #1  ;@ Desloca quociente
	movs r1, r1, lsl #1 ;@ Desloca dividendo
	add r4, r4, #1
	bcc _carry_zero
	add r2, r2, #1      ;@ Soma 1 a parcela quando o carry eh 1
_carry_zero:
	cmp r2, r0
	bge _subtracao      ;@ Parcela maior ou igual ao divisor, subtrai o valor do divisor dele
	b _desloca
_subtracao:
	sub r2, r2, r0
	add r3, r3, #1
	b _desloca
_end_divisao:
	mov pc, lr          ;@ Retorno