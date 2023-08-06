; RUN: llvm-mutate -f %s -p U8.OP0,C0 -p U10.OP0,C1 2>&1 | filecheck %s
; CHECK:        opreplaced U8.OP0,C0
; CHECK:        opreplaced U10.OP0,C1
; CHECK:        br i1 false
; CHECK:        br i1 true

define dso_local void @_Z4axpyfPfS_(float %A1, float* nocapture readonly %A2, float* nocapture %A3) {
  %U1 = tail call i32 @llvm.nvvm.read.ptx.sreg.tid.x(), !uniqueID !0
  %U2 = zext i32 %U1 to i64, !uniqueID !1
  %U3 = getelementptr inbounds float, float* %A2, i64 %U2, !uniqueID !2
  %U4 = load float, float* %U3, align 4, !uniqueID !3
  %U5 = fmul contract float %U4, %A1, !uniqueID !4
  %U6 = fadd contract float %U4, %U5, !uniqueID !5
  %U7 = icmp eq i64 %U2, 0, !uniqueID !6
  br i1 %U7, label %1, label %2, !uniqueID !7
; <label>:1:
  store float %U6, float* %U3, align 4, !uniqueID !8
  br i1 %U7, label %2, label %1, !uniqueID !9
; <label>:2:
  ret void, !uniqueID !10
}

; Function Attrs: nounwind readnone
declare i32 @llvm.nvvm.read.ptx.sreg.tid.x() #0

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
!9 = !{!"U10"}
!10 = !{!"U11"}
