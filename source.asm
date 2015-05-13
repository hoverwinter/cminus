TITLE sum of array

.686P
.MODEL FLAT,STDCALL
.STACK 4096
option casemap:none

INCLUDELIB MSVCRT.LIB
INCLUDELIB KERNEL32.LIB


scanf PROTO C,: PTR BYTE,: VARARG
printf PROTO C,:PTR BYTE,: VARARG
getchar PROTO C
ExitProcess PROTO,:DWORD

.data
t0 dword ?
t1 dword ?
t2 dword ?
t3 dword ?
t4 dword ?
t5 dword ?
t6 dword ?
t7 dword ?
t8 dword ?
t9 dword ?
t10 dword ?
t11 dword ?
t12 dword ?
i dword ?
k dword ?
temp dword ?
credit dword 2,2,1,2,2,3
stu_number dword ?
sum dword ?
mean dword ?
score dword 76,82,90,86,79,62
msg byte "please input your student number:",0
msg1 byte "%d",0
msg2 byte "the score of student number  %d is %d higher than 60.\n",0
msg3 byte "the score of student number %d is %d lower than 60.\n",0
msg4 byte "sum: %d",0
.code
calc PROC uses eax,a:DWORD, b: DWORD
mov eax,a
add eax,b
mov t0,eax
mov eax,t0
mov k,eax
ret
calc ENDP

main PROC
invoke printf,offset msg
invoke scanf,offset msg1,offset stu_number
mov eax,0
mov sum,eax
mov eax,0
mov temp,eax
mov eax,0
mov i,eax
L15:cmp i,6
jl L20
jmp L49
L18:inc i
jmp L15
L20:mov eax,i
mov ebx,4
mul ebx
mov t1,eax
mov eax,score[eax]
mov t2,eax
mov eax,i
mov ebx,4
mul ebx
mov t3,eax
mov eax,credit[eax]
mov t4,eax
mov eax,t2
mov ebx,t4
mul ebx
mov t5,eax
mov eax,sum
add eax,t5
mov t6,eax
mov eax,t6
mov sum,eax
mov eax,i
mov ebx,4
mul ebx
mov t7,eax
mov eax,credit[eax]
mov t8,eax
mov eax,temp
add eax,t8
mov t9,eax
mov eax,t9
mov temp,eax
jmp L18
L49:mov eax,sum
mov ebx,temp
div temp
mov t10,eax
mov eax,t10
mov mean,eax
cmp mean,60
jge L57
jmp L64
L57:mov eax,mean
sub eax,60
mov t11,eax
mov eax,t11
mov mean,eax
invoke printf,offset msg2,stu_number,mean
jmp L70
L64:mov eax,60
sub eax,mean
mov t12,eax
mov eax,t12
mov mean,eax
invoke printf,offset msg3,stu_number,mean
L70:invoke calc,mean,temp
mov i,eax
invoke printf,offset msg4,i
invoke getchar
ret 0
main ENDP
END main
