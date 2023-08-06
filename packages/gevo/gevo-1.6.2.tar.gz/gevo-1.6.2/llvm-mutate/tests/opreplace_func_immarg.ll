; RUN: llvm-mutate --not_use_result -f %s -p U1.OP0,C1 -p U1.OP0,A4 2>&1 | filecheck %s
; CHECK:        opreplaced U1.OP0,C1
; CHECK:        oprepl failed(U1.OP0,A4). dest operand U1.OP0 is a function argument with immarg attribute

define dso_local void @_Z4axpyfPfS_(float %A1, float* nocapture readonly %A2, float* nocapture %A3, i8 %A4) {
  tail call void @llvm.ubsantrap(i8 0), !uniqueID !0
  %U2 = zext i8 0 to i64, !uniqueID !1
  %U3 = getelementptr inbounds float, float* %A2, i64 %U2, !uniqueID !2
  %U4 = load float, float* %U3, align 4, !uniqueID !3
  %U5 = fmul contract float %U4, %A1, !uniqueID !4
  %U6 = fadd contract float %U4, %U5, !uniqueID !5
  %U7 = getelementptr inbounds float, float* %A3, i64 %U2, !uniqueID !6
  store float %U6, float* %U7, align 4, !uniqueID !7
  ret void, !uniqueID !8
}

; Function Attrs: nounwind readnone
declare void @llvm.ubsantrap(i8 immarg) cold noreturn nounwind

attributes #0 = { nounwind readnone }

!0 = !{!"U1"}
!1 = !{!"U2"}
!2 = !{!"U3"}
!3 = !{!"U4"}
!4 = !{!"U5"}
!5 = !{!"U6"}
!6 = !{!"U7"}
!7 = !{!"U8"}
!8 = !{!"U9"}
