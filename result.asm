TITLE hoverwinter@gmail.com 2015

.686P
.MODEL FLAT,STDCALL
.STACK 4096
option casemap:none

INCLUDELIB MSVCRT.LIB
INCLUDELIB KERNEL32.LIB

scanf PROTO C,: PTR BYTE,: VARARG
printf PROTO C,:PTR BYTE,: VARARG

.data
fmt4 byte "sum: %d",0
fmt3 byte "the score of student number %d is %d lower than 60.",0dh,0ah,0
fmt2 byte "the score of student number  %d is %d higher than 60.",0dh,0ah,0
fmt1 byte "%d",0
fmt0 byte "please input your student number:",0
k dword ?
score dword 76,82,90,86,79,62
i dword ?
temp dword ?
sum dword ?
mean dword ?
stu_number dword ?
credit dword 2,2,1,2,2,3
t12 dword ?
t11 dword ?
t10 dword ?
t9 dword ?
t8 dword ?
t7 dword ?
t6 dword ?
t5 dword ?
t4 dword ?
t3 dword ?
t2 dword ?
t1 dword ?
t0 dword ?
.code
calc PROC uses eax ebx , a: dword, b: dword
mov eax,a
add eax,b
mov t0,eax
mov eax,t0
mov k,eax
mov eax,k
ret
calc ENDP
main PROC
invoke printf,offset fmt0 
invoke scanf,offset fmt1 ,offset stu_number
mov eax,0
mov sum,eax
mov eax,0
mov temp,eax
mov eax,0
mov i,eax
L16:cmp i,6
jl L21
jmp L57
L19:inc i
jmp L16
L21:mov eax,i
mov ebx,4
mul ebx
mov t1,eax
mov ecx,t1
mov eax,score[ecx]
mov t2,eax
mov eax,i
mov ebx,4
mul ebx
mov t3,eax
mov ecx,t3
mov eax,credit[ecx]
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
mov ecx,t7
mov eax,credit[ecx]
mov t8,eax
mov eax,temp
add eax,t8
mov t9,eax
mov eax,t9
mov temp,eax
jmp L19
L57:mov eax,sum
mov ebx,temp
div ebx
mov t10,eax
mov eax,t10
mov mean,eax
cmp mean,60
jge L66
jmp L73
L66:mov eax,mean
sub eax,60
mov t11,eax
mov eax,t11
mov mean,eax
invoke printf,offset fmt2 ,stu_number,mean
jmp L79
L73:mov eax,60
sub eax,mean
mov t12,eax
mov eax,t12
mov mean,eax
invoke printf,offset fmt3 ,stu_number,mean
L79:invoke calc,mean,temp
mov i,eax
invoke printf,offset fmt4 ,i
mov eax,0
ret
main ENDP
END main
