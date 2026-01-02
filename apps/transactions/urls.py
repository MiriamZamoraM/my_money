from django.urls import path
from . import views

urlpatterns = [
   

   path('concepts/', views.RegisterConceptView.as_view(),), #Crea un nuevo concepto.
   path('colors/', views.RegisterColorView.as_view(),), #Crea un nuevo color.
   path('regmov/', views.RegisterMoveView.as_view(),), #Registra un movimiento (ingreso, egreso).
  
   path('all/', views.ListMoveView.as_view(),), #Lista todos los movimientos.
   path('concepts/all/', views.ListConceptsView.as_view(),), #Lista todos los conceptos.
   path('concepts/color/<int:color>/', views.ListConceptColorView.as_view(),), #Lista los conceptos por color.
   path('concepts/concept/<int:pk>/', views.ListConceptIdView.as_view(),), #Lista los conceptos por id.
   path('concepts/spents/', views.ListConceptSpentView.as_view(),), #Lista los conceptos por gastos.
   path('concepts/incomes/', views.ListConceptIncomeView.as_view(),), #Lista los conceptos por ingresos.
   path('concepts/fixed/', views.ListConceptFixedView.as_view(),), #Lista los conceptos fijos.
   path('concepts/variable/', views.ListConceptVariableView.as_view(),), #Lista los conceptos variables.

   path('spents/', views.ListMoveSpentView.as_view(),), #Lista los movimientos por gastos.
   path('spents/month/<str:month>/', views.ListMoveSpentMonthView.as_view(),), #Lista los gastos por mes.
   path('spents/year/<str:year>/', views.ListMoveSpentYearView.as_view(),), #Lista los gastos por año.
   path('spents/day/<str:day>/', views.ListMoveSpentDayView.as_view(),), #Lista los gastos por día.
   path('spents/week/<str:week>/', views.ListMoveSpentWeekView.as_view(),), #Lista los gastos por semana.
   path('spents/variable/', views.ListMoveSpentVariableView.as_view(),), #Lista los gastos variables.
   path('spents/fixed/', views.ListMoveSpentFijoView.as_view(),), #Lista los gastos fijos.
   path('spents/color/<int:pk>/', views.ListMoveSpentColorView.as_view(),), #Lista los gastos por color.


   path('uds/<int:move_id>/', views.CRUDMoveAPIView.as_view(),), #Edita un gasto.

   path('incomes/', views.ListMoveIncomeView.as_view(),), #Lista los movimientos por ingresos.
   path('incomes/month/<str:month>/', views.ListMoveIncomeMonthView.as_view(),), #Lista los ingresos por mes.
   path('incomes/year/<str:year>/', views.ListMoveIncomeYearView.as_view(),), #Lista los ingresos por año.
   path('incomes/day/<str:day>/', views.ListMoveIncomeDayView.as_view(),), #Lista los ingresos por día.
   path('incomes/week/<str:week>/', views.ListMoveIncomeWeekView.as_view(),), #Lista los ingresos por semana
   path('incomes/variable/', views.ListMoveIncomeVariableView.as_view(),), #Lista los ingresos variables.
   path('incomes/fixed/', views.ListMoveIncomeFijoView.as_view(),), #Lista los ingresos fijos.
   path('incomes/color/<int:pk>/', views.ListMoveIncomeColorView.as_view(),), #Lista los ingresos por color.

   path('udi/<int:move_id>/', views.CRUDMoveIncomeAPIView.as_view(),), #Edita un ingreso.

   path('balance/month/<str:month>/', views.ListBalanceMonthView.as_view(),), #Lista balance por mes con suma.
   path('balance/week/<str:week>/', views.ListBalanceWeekView.as_view(),), #Lista balance por semana con suma.
   path('balance/year/<str:year>/', views.ListBalanceYearView.as_view(),), #Lista balance por año con suma.
   path('balance/weekandyear/<str:week>/<str:year>/', views.ListBalanceWeekYearView.as_view(),), #Lista balance de la semana y año específico
   path('balance/monthandyear/<str:month>/<str:year>/', views.ListBalanceMonthYearView.as_view(),), #lista del balance del mes y año específico
   path('balance/day/<str:day>/', views.ListBalanceDayView.as_view(),), #Lista balance por día con suma.
   path('balance/all/moves/', views.ListBalanceMoveView.as_view(),), #Lista balance con ingresos y gastos con suma y resta.
   path('balance/fixed/moves/', views.ListBalanceFixedView.as_view(),), #Lista balance con ingresos y gastos fijos con suma y resta.
   path('balance/variable/moves/', views.ListBalanceVariableView.as_view(),), #Lista balance con ingresos y gastos variables con suma y resta.
   path('balance/spents/', views.ListBalanceSpentView.as_view(),), #Lista el balance de gastos con suma.
   path('balance/incomes/', views.ListBalanceIncomeView.as_view(),), #Lista el balance de ingresos.
   

   path('balance/account/<int:pk>/month/<str:month>/', views.ListBalanceAccountMonthView.as_view(),), #Lista balance de una cuenta y por mes.
   path('balance/account/<int:pk>/week/<str:week>/', views.ListBalanceAccountWeekView.as_view(),), #Lista balance de una cuenta y por semana.
   path('balance/account/<int:pk>/year/<str:year>/', views.ListBalanceAccountYearView.as_view(),), #Lista balance de una cuenta y por año.
   path('balance/account/<int:pk>/monthandyear/<str:month>/<str:year>/', views.ListBalanceAccountMonthYearView.as_view(),), #Lista balance de una cuenta por mes y año específico
   path('balance/account/<int:pk>/weekandyear/<str:week>/<str:year>/', views.ListBalanceAccountWeekYearView.as_view(),), #Lista balance de una cuenta por semana y año específico
   path('balance/account/<int:pk>/day/<str:day>/', views.ListBalanceAccountDayView.as_view(),), #Lista balance de una cuenta y por day.
   path('balance/account/<int:pk>/', views.ListBalanceAccountMoveView.as_view(),), #Lista balance de una cuenta y por ingresos y gastos.
   path('balance/account/fixed/<int:pk>/', views.ListBalanceAccountFixedMoveView.as_view(),), #Lista balance de una cuenta y por ingresos y gastos fijos.
   path('balance/account/variable/<int:pk>/', views.ListBalanceAccountVariableMoveView.as_view(),), #Lista balance de una cuenta y por ingresos y gastos variables.
   path('balance/account/spents/<int:pk>/', views.ListBalanceAccountSpentView.as_view(),), #Lista balance de gastos de una cuenta.
   path('balance/account/incomes/<int:pk>/', views.ListBalanceAccountIncomeView.as_view(),), #Lista balance de ingresos de una cuenta.

]