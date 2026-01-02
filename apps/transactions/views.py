from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Concept, Move, Color
from .serializers import ConceptSerializer,MoveSerializer, ColorSerializer, BalanceMoveSerializer, MoveSpentColorSerializer
from django.db.models import Sum

# Create your views here.

# Esta clase es para crear un nuevo concepto
class RegisterConceptView(APIView):
    permission_classes=(IsAuthenticated,)

    def post(self, request):
        data = request.data
        data['user_id'] = request.user.id
        serializer = ConceptSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Esta clase es para registrar un nuevo color.
class RegisterColorView(APIView):
    permission_classes=(IsAuthenticated,)

    def post(self, request):
        data = request.data
        serializer = ColorSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# ELIMINA COLORES    
class DeleteColorAPIView(APIView):
    permission_classes = (IsAuthenticated,)  

    def delete(self, request, pk):
        Color.objects.filter(pk=pk).delete()
        return Response({'message':'Eliminado'}, status=status.HTTP_204_NO_CONTENT)

# EDITA CONCEPTOS
class EditConceptosAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self, request, pk):
        concept_obj = get_object_or_404(Concept, pk=pk, user=request.user)
        serializer = ConceptSerializer(instance=concept_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# Esta clase es para registrar un movimiento (ingreso o gasto)    
class RegisterMoveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = MoveSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Esta clase es para listar los movimientos
class ListMoveView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request):
        move_list = Move.objects.filter(concept__user=request.user, status_delete=False)
        serializer = MoveSerializer(move_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Esta vista es para listar los conceptos.
class ListConceptsView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request):
        concept_list = Concept.objects.filter(user=request.user, status_delete=False)
        serializer = ConceptSerializer(concept_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Esta vista es para listar los conceptos por color.
class ListConceptColorView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, color):
        queryset = Concept.objects.filter(color=color, user=request.user.id)
        #concepts = queryset.concept_set.all()
        serializer = ConceptSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Esta vista es para listar los conceptos por id.
class ListConceptIdView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, pk):
        queryset = Concept.objects.filter(pk=pk, status_delete=False, user=request.user.id)
        serializer = ConceptSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Esta vista es para listar los conceptos por gastos.
class ListConceptSpentView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request):
        queryset = Concept.objects.filter(type_movement='gasto', status_delete=False, user=request.user)
        serializer = ConceptSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Esta vista es para listar los conceptos por ingresos.
class ListConceptIncomeView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request):
        queryset = Concept.objects.filter(type_movement='ingreso', status_delete=False, user=request.user)
        serializer = ConceptSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Esta vista es para listar los conceptos (gastos o ingresos) fijos.
class ListConceptFixedView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request):
        queryset = Concept.objects.filter(type_clasification='fijo', status_delete=False, user=request.user)
        serializer = ConceptSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Esta vista es para listar los conceptos (gastos o ingresos) variables.
class ListConceptVariableView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request):
        queryset_v = Concept.objects.filter(type_clasification='variable', status_delete=False, user=request.user)
        serializer_v = ConceptSerializer(queryset_v, many=True)
        return Response(serializer_v.data, status=status.HTTP_200_OK)



# Esta vista es para listar los movimientos por gastos.
class ListMoveSpentView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request):
        queryset = Move.objects.filter(concept__type_movement='gasto', status_delete=False, concept__user=request.user)
        serializer = MoveSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Esta vista es para listar los gastos por mes.
class ListMoveSpentMonthView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, month):
        queryset = Move.objects.filter(day__month=month, concept__type_movement='gasto', status_delete=False, concept__user=request.user)
        serializer = MoveSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Esta vista es para listar los gastos por año.
class ListMoveSpentYearView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, year):
        queryset = Move.objects.filter(day__year=year, concept__type_movement='gasto', status_delete=False, concept__user=request.user)
        serializer = MoveSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Esta vista es para listar los gastos por día del año.
class ListMoveSpentDayView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, day):
        queryset = Move.objects.filter(day=day, concept__type_movement='gasto', status_delete=False, concept__user=request.user)
        serializer = MoveSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Esta vista es para listar los gastos por semana del año.
class ListMoveSpentWeekView(APIView):
    permission_classes=(IsAuthenticated,) 

    def get(self, request, week):
        queryset = Move.objects.filter(day__week=week, concept__type_movement='gasto', status_delete=False, concept__user=request.user)
        serializer = MoveSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Esta vista es para listar los gastos variables.
class ListMoveSpentVariableView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request):
        queryset = Move.objects.filter(concept__user=request.user, concept__type_clasification='variable', concept__type_movement='gasto', status_delete=False)
        serializer = MoveSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Esta vista es para listar los gastos fijos.
class ListMoveSpentFijoView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request):
        queryset = Move.objects.filter(concept__user=request.user, concept__type_clasification='fijo', concept__type_movement='gasto', status_delete=False)
        serializer = MoveSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Esta vista es para listar los gastos por color.
class ListMoveSpentColorView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, pk):
        queryset = Move.objects.filter(concept__user=request.user, concept__type_movement='gasto', concept__color__id=pk, status_delete=False)
        serializer = MoveSpentColorSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# Clase para editar y eliminar movimientos
class CRUDMoveAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, move_id):
        move_obj = get_object_or_404(Move, pk=move_id, concept__type_movement='gasto', status_delete=False, concept__user=request.user)
        serializer = MoveSerializer(instance=move_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, move_id):
        account_obj = get_object_or_404(Move, pk=move_id, concept__type_movement='gasto', status_delete=False, concept__user=request.user)
        account_obj.status_delete = True
        account_obj.save()
        return Response({'message':'Eliminado'}, status=status.HTTP_204_NO_CONTENT)
    

# Esta vista es para listar los movimientos por ingresos.
class ListMoveIncomeView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request):
        queryset = Move.objects.filter(concept__type_movement='ingreso', status_delete=False, concept__user=request.user)
        serializer = MoveSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Esta vista es para listar los ingresos por mes.
class ListMoveIncomeMonthView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, month):
        queryset = Move.objects.filter(day__month=month, concept__type_movement='ingreso', status_delete=False, concept__user=request.user)
        serializer = MoveSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Esta vista es para listar los ingresos por año.
class ListMoveIncomeYearView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, year):
        queryset = Move.objects.filter(day__year=year, concept__type_movement='ingreso', status_delete=False, concept__user=request.user)
        serializer = MoveSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Esta vista es para listar los ingresos por día del año.
class ListMoveIncomeDayView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, day):
        queryset = Move.objects.filter(concept__user=request.user, day=day, concept__type_movement='ingreso', status_delete=False)
        serializer = MoveSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Esta vista es para listar los ingresos por semana del año.
class ListMoveIncomeWeekView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, week):
        queryset = Move.objects.filter(concept__user=request.user, day__week=week, concept__type_movement='ingreso', status_delete=False)
        serializer = MoveSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Esta vista es para listar los ingresos variables.
class ListMoveIncomeVariableView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request):
        queryset = Move.objects.filter(concept__user=request.user, concept__type_clasification='variable', concept__type_movement='ingreso', status_delete=False)
        serializer = MoveSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Esta vista es para listar los ingresos fijos.
class ListMoveIncomeFijoView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request):
        queryset = Move.objects.filter(concept__user=request.user, concept__type_clasification='fijo', concept__type_movement='ingreso', status_delete=False)
        serializer = MoveSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Esta vista es para listar los ingresos por color.
class ListMoveIncomeColorView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, pk):
        queryset = Move.objects.filter(concept__user=request.user, concept__type_movement='ingreso', concept__color__id=pk, status_delete=False)
        serializer = MoveSpentColorSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        
# Esta vista edita un solo ingreso.
class CRUDMoveIncomeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, move_id):
        move_obj = get_object_or_404(Move, pk=move_id, concept__type_movement='ingreso', status_delete=False, concept__user=request.user)
        serializer = MoveSerializer(instance=move_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, move_id):
        account_obj = get_object_or_404(Move, pk=move_id, concept__type_movement='ingreso', concept__user=request.user)
        account_obj.status_delete = True
        account_obj.save()
        return Response({'message':'Eliminado'}, status=status.HTTP_204_NO_CONTENT)
        

#BALANCE GENERAL
#         
# Esta vista es para listar balance solo mes sin año con suma
class ListBalanceMonthView(APIView):
    permission_classes=(IsAuthenticated,) 

    def get(self, request, month):
        ingresos_list = Move.objects.filter(day__month=month, concept__type_movement='ingreso', status_delete=False, concept__user=request.user)
        ingresos_total = Move.objects.filter(day__month=month, concept__type_movement='ingreso', status_delete=False, concept__user=request.user).aggregate(Sum('amount'))
        gastos_list = Move.objects.filter(day__month=month, concept__type_movement='gasto', status_delete=False, concept__user=request.user)
        gastos_total = Move.objects.filter(day__month=month, concept__type_movement='gasto', status_delete=False, concept__user=request.user).aggregate(Sum('amount'))
        serializer_ingresos = BalanceMoveSerializer(ingresos_list, many=True)
        serializer_gastos = BalanceMoveSerializer(gastos_list, many=True)
      
        balance = 0
        ingresos = ingresos_total.get("amount__sum", None)
        gastos = gastos_total.get("amount__sum", None)
        if ingresos is not None and gastos is not None:
            balance = ingresos-gastos
            data = { "account_incomes" : serializer_ingresos.data,
                     "account_spents" : serializer_gastos.data,
                     "balance": balance}
            return Response(data, status=status.HTTP_200_OK)
        elif ingresos is None and gastos is None:
            return Response({'No hay ingresos y tampoco gastos'}, status=status.HTTP_200_OK)        
        elif ingresos is None:
            balance = balance-gastos
            data = {
                "Message" : "No hay ingresos en este periodo",
                "account_spents" : serializer_gastos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)
        elif gastos is None:
            balance = balance+ingresos
            data = {
                "Message" : "No hay gastos en este periodo",
                "account_incomes" : serializer_ingresos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)


# Esta vista es para listar balance por año con suma.
class ListBalanceYearView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, year):
        ingresos_list = Move.objects.filter(day__year=year, concept__type_movement='ingreso', status_delete=False, concept__user=request.user)
        ingresos_total = Move.objects.filter(day__year=year, concept__type_movement='ingreso', status_delete=False, concept__user=request.user).aggregate(Sum('amount'))
        gastos_list = Move.objects.filter(day__year=year, concept__type_movement='gasto', status_delete=False, concept__user=request.user)
        gastos_total = Move.objects.filter(day__year=year, concept__type_movement='gasto', status_delete=False, concept__user=request.user).aggregate(Sum('amount'))
        serializer_ingresos = BalanceMoveSerializer(ingresos_list, many=True)
        serializer_gastos = BalanceMoveSerializer(gastos_list, many=True)

        balance = 0
        ingresos = ingresos_total.get("amount__sum", None)
        gastos = gastos_total.get("amount__sum", None)
        if ingresos is not None and gastos is not None:
            balance = ingresos-gastos
            data = { "account_incomes" : serializer_ingresos.data,
                     "account_spents" : serializer_gastos.data,
                     "balance": balance}
            return Response(data, status=status.HTTP_200_OK)
        elif ingresos is None and gastos is None:
            return Response({'No hay ingresos y tampoco gastos'}, status=status.HTTP_200_OK)        
        elif ingresos is None:
            balance = balance-gastos
            data = {
                "Message" : "No hay ingresos en este periodo",
                "account_spents" : serializer_gastos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)
        elif gastos is None:
            balance = balance+ingresos
            data = {
                "Message" : "No hay gastos en este periodo",
                "account_incomes" : serializer_ingresos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)

# Esta vista es para listar balance por semana del año con suma.
class ListBalanceWeekView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, week):
        ingresos_list = Move.objects.filter(day__week=week, concept__type_movement='ingreso', status_delete=False, concept__user=request.user)
        ingresos_total = Move.objects.filter(day__week=week, concept__type_movement='ingreso', status_delete=False, concept__user=request.user).aggregate(Sum('amount'))
        gastos_list = Move.objects.filter(day__week=week, concept__type_movement='gasto', status_delete=False, concept__user=request.user)
        gastos_total = Move.objects.filter(day__week=week, concept__type_movement='gasto', status_delete=False, concept__user=request.user).aggregate(Sum('amount'))
        serializer_ingresos = BalanceMoveSerializer(ingresos_list, many=True)
        serializer_gastos = BalanceMoveSerializer(gastos_list, many=True)

        balance = 0
        ingresos = ingresos_total.get("amount__sum", None)
        gastos = gastos_total.get("amount__sum", None)
        if ingresos is not None and gastos is not None:
            balance = ingresos-gastos
            data = { "account_incomes" : serializer_ingresos.data,
                     "account_spents" : serializer_gastos.data,
                     "balance": balance}
            return Response(data, status=status.HTTP_200_OK)
        elif ingresos is None and gastos is None:
            return Response({'No hay ingresos y tampoco gastos'}, status=status.HTTP_200_OK)        
        elif ingresos is None:
            balance = balance-gastos
            data = {
                "Message" : "No hay ingresos en este periodo",
                "account_spents" : serializer_gastos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)
        elif gastos is None:
            balance = balance+ingresos
            data = {
                "Message" : "No hay gastos en este periodo",
                "account_incomes" : serializer_ingresos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)


# Esta vista es para listar balance por día del año con suma.
class ListBalanceDayView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, day):
        ingresos_list = Move.objects.filter(day=day, concept__type_movement='ingreso', status_delete=False, concept__user=request.user)
        ingresos_total = Move.objects.filter(day=day, concept__type_movement='ingreso', status_delete=False, concept__user=request.user).aggregate(Sum('amount'))
        gastos_list = Move.objects.filter(day=day, concept__type_movement='gasto', status_delete=False, concept__user=request.user)
        gastos_total = Move.objects.filter(day=day, concept__type_movement='gasto', status_delete=False, concept__user=request.user).aggregate(Sum('amount'))
        serializer_ingresos = BalanceMoveSerializer(ingresos_list, many=True)
        serializer_gastos = BalanceMoveSerializer(gastos_list, many=True)

        balance = 0
        ingresos = ingresos_total.get("amount__sum", None)
        gastos = gastos_total.get("amount__sum", None)
        if ingresos is not None and gastos is not None:
            balance = ingresos-gastos
            data = { "account_incomes" : serializer_ingresos.data,
                     "account_spents" : serializer_gastos.data,
                     "balance": balance}
            return Response(data, status=status.HTTP_200_OK)
        elif ingresos is None and gastos is None:
            return Response({'No hay ingresos y tampoco gastos'}, status=status.HTTP_200_OK)        
        elif ingresos is None:
            balance = balance-gastos
            data = {
                "Message" : "No hay ingresos en este periodo",
                "account_spents" : serializer_gastos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)
        elif gastos is None:
            balance = balance+ingresos
            data = {
                "Message" : "No hay gastos en este periodo",
                "account_incomes" : serializer_ingresos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)


class ListBalanceWeekYearView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, week, year):
        ingresos_list = Move.objects.filter(day__week=week, day__year=year, concept__type_movement='ingreso', status_delete=False, concept__user=request.user)
        ingresos_total = Move.objects.filter(day__week=week, day__year=year, concept__type_movement='ingreso', status_delete=False, concept__user=request.user).aggregate(Sum('amount'))
        gastos_list = Move.objects.filter(day__week=week, day__year=year, concept__type_movement='gasto', status_delete=False, concept__user=request.user)
        gastos_total = Move.objects.filter(day__week=week, day__year=year, concept__type_movement='gasto', status_delete=False, concept__user=request.user).aggregate(Sum('amount'))
        serializer_ingresos = BalanceMoveSerializer(ingresos_list, many=True)
        serializer_gastos = BalanceMoveSerializer(gastos_list, many=True)

        balance = 0
        ingresos = ingresos_total.get("amount__sum", None)
        gastos = gastos_total.get("amount__sum", None)
        if ingresos is not None and gastos is not None:
            balance = ingresos-gastos
            data = { "account_incomes" : serializer_ingresos.data,
                     "account_spents" : serializer_gastos.data,
                     "balance": balance}
            return Response(data, status=status.HTTP_200_OK)
        elif ingresos is None and gastos is None:
            return Response({'No hay ingresos y tampoco gastos'}, status=status.HTTP_200_OK)        
        elif ingresos is None:
            balance = balance-gastos
            data = {
                "Message" : "No hay ingresos en este periodo",
                "account_spents" : serializer_gastos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)
        elif gastos is None:
            balance = balance+ingresos
            data = {
                "Message" : "No hay gastos en este periodo",
                "account_incomes" : serializer_ingresos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)
       

class ListBalanceMonthYearView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, month, year):
        ingresos_list = Move.objects.filter(day__month=month, day__year=year, concept__type_movement='ingreso', status_delete=False, concept__user=request.user)
        ingresos_total = Move.objects.filter(day__month=month, day__year=year, concept__type_movement='ingreso', status_delete=False, concept__user=request.user).aggregate(Sum('amount'))
        gastos_list = Move.objects.filter(day__month=month, day__year=year, concept__type_movement='gasto', status_delete=False, concept__user=request.user)
        gastos_total = Move.objects.filter(day__month=month, day__year=year, concept__type_movement='gasto', status_delete=False, concept__user=request.user).aggregate(Sum('amount'))
        serializer_ingresos = BalanceMoveSerializer(ingresos_list, many=True)
        serializer_gastos = BalanceMoveSerializer(gastos_list, many=True)

        balance = 0
        ingresos = ingresos_total.get("amount__sum", None)
        gastos = gastos_total.get("amount__sum", None)
        if ingresos is not None and gastos is not None:
            balance = ingresos-gastos
            data = { "account_incomes" : serializer_ingresos.data,
                     "account_spents" : serializer_gastos.data,
                     "balance": balance}
            return Response(data, status=status.HTTP_200_OK)
        elif ingresos is None and gastos is None:
            return Response({'No hay ingresos y tampoco gastos'}, status=status.HTTP_200_OK)        
        elif ingresos is None:
            balance = balance-gastos
            data = {
                "Message" : "No hay ingresos en este periodo",
                "account_spents" : serializer_gastos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)
        elif gastos is None:
            balance = balance+ingresos
            data = {
                "Message" : "No hay gastos en este periodo",
                "account_incomes" : serializer_ingresos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)

# Esta vista es para listar balance con ingresos y gastos con suma y resta.
class ListBalanceMoveView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request):
        ingresos_list = Move.objects.filter(concept__type_movement='ingreso', status_delete=False, concept__user=request.user)
        ingresos_total = Move.objects.filter(concept__type_movement='ingreso', status_delete=False, concept__user=request.user).aggregate(Sum('amount'))
        gastos_list = Move.objects.filter(concept__type_movement='gasto', status_delete=False, concept__user=request.user)
        gastos_total = Move.objects.filter(concept__type_movement='gasto', status_delete=False, concept__user=request.user).aggregate(Sum('amount'))
        serializer_ingresos = BalanceMoveSerializer(ingresos_list, many=True)
        serializer_gastos = BalanceMoveSerializer(gastos_list, many=True)

        balance = 0
        ingresos = ingresos_total.get("amount__sum", None)
        gastos = gastos_total.get("amount__sum", None)
        if ingresos is not None and gastos is not None:
            balance = ingresos-gastos
            data = { "account_incomes" : serializer_ingresos.data,
                     "account_spents" : serializer_gastos.data,
                     "balance": balance}
            return Response(data, status=status.HTTP_200_OK)
        elif ingresos is None and gastos is None:
            return Response({'No hay ingresos y tampoco gastos'}, status=status.HTTP_200_OK)        
        elif ingresos is None:
            balance = balance-gastos
            data = {
                "Message" : "No hay ingresos en este periodo",
                "account_spents" : serializer_gastos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)
        elif gastos is None:
            balance = balance+ingresos
            data = {
                "Message" : "No hay gastos en este periodo",
                "account_incomes" : serializer_ingresos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)

# Esta vista es para listar balance (gastos y los ingresos) fijos con suma y resta.
class ListBalanceFixedView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request):
        ingresos_list = Move.objects.filter(concept__type_clasification='fijo', concept__type_movement='ingreso', status_delete=False, concept__user=request.user)
        gastos_list = Move.objects.filter(concept__type_clasification='fijo', concept__type_movement='gasto', status_delete=False, concept__user=request.user)
        ingresos_total = Move.objects.filter(concept__type_clasification='fijo', concept__type_movement='ingreso', status_delete=False, concept__user=request.user).aggregate(Sum('amount'))
        gastos_total = Move.objects.filter(concept__type_clasification='fijo', concept__type_movement='gasto', status_delete=False, concept__user=request.user).aggregate(Sum('amount'))
        serializer_ingresos = BalanceMoveSerializer(ingresos_list, many=True)
        serializer_gastos = BalanceMoveSerializer(gastos_list, many=True)

        balance = 0
        ingresos = ingresos_total.get("amount__sum", None)
        gastos = gastos_total.get("amount__sum", None)
        if ingresos is not None and gastos is not None:
            balance = ingresos-gastos
            data = { "account_incomes" : serializer_ingresos.data,
                     "account_spents" : serializer_gastos.data,
                     "balance": balance}
            return Response(data, status=status.HTTP_200_OK)
        elif ingresos is None and gastos is None:
            return Response({'No hay ingresos y tampoco gastos'}, status=status.HTTP_200_OK)        
        elif ingresos is None:
            balance = balance-gastos
            data = {
                "Message" : "No hay ingresos en este periodo",
                "account_spents" : serializer_gastos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)
        elif gastos is None:
            balance = balance+ingresos
            data = {
                "Message" : "No hay gastos en este periodo",
                "account_incomes" : serializer_ingresos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)

# Esta vista es para listar balance (gastos y los ingresos) variables.
class ListBalanceVariableView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request):
        ingresos_list = Move.objects.filter(concept__type_clasification='variable', concept__type_movement='ingreso', status_delete=False, concept__user=request.user)
        gastos_list = Move.objects.filter(concept__type_clasification='variable', concept__type_movement='gasto', status_delete=False, concept__user=request.user)
        ingresos_total = Move.objects.filter(concept__type_clasification='variable', concept__type_movement='ingreso', status_delete=False, concept__user=request.user).aggregate(Sum('amount'))
        gastos_total = Move.objects.filter(concept__type_clasification='variable', concept__type_movement='gasto', status_delete=False, concept__user=request.user).aggregate(Sum('amount'))
        serializer_ingresos = BalanceMoveSerializer(ingresos_list, many=True)
        serializer_gastos = BalanceMoveSerializer(gastos_list, many=True)

        balance = 0
        ingresos = ingresos_total.get("amount__sum", None)
        gastos = gastos_total.get("amount__sum", None)
        if ingresos is not None and gastos is not None:
            balance = ingresos-gastos
            data = { "account_incomes" : serializer_ingresos.data,
                     "account_spents" : serializer_gastos.data,
                     "balance": balance}
            return Response(data, status=status.HTTP_200_OK)
        elif ingresos is None and gastos is None:
            return Response({'No hay ingresos y tampoco gastos'}, status=status.HTTP_200_OK)        
        elif ingresos is None:
            balance = balance-gastos
            data = {
                "Message" : "No hay ingresos en este periodo",
                "account_spents" : serializer_gastos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)
        elif gastos is None:
            balance = balance+ingresos
            data = {
                "Message" : "No hay gastos en este periodo",
                "account_incomes" : serializer_ingresos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)

# Esta vista es para listar el balance de gastos con suma.
class ListBalanceSpentView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request):
        gastos_list = Move.objects.filter(concept__type_movement='gasto', status_delete=False, concept__user=request.user)
        gastos_total = Move.objects.filter(concept__type_movement='gasto', status_delete=False, concept__user=request.user).aggregate(Sum('amount'))
        serializer_gastos = MoveSerializer(gastos_list, many=True)

        data = { "account_spents" : serializer_gastos.data,
        "balance": gastos_total
        }

        return Response(data, status=status.HTTP_200_OK)

# Esta vista es para listar el balance de ingresos con suma.
class ListBalanceIncomeView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request):
        ingresos_list = Move.objects.filter(concept__type_movement='ingreso', status_delete=False, concept__user=request.user)
        ingresos_total = Move.objects.filter(concept__type_movement='ingreso', status_delete=False, concept__user=request.user).aggregate(Sum('amount'))
        serializer_ingresos = MoveSerializer(ingresos_list, many=True)

        data = { "account_incomes" : serializer_ingresos.data,
        "balance": ingresos_total
        }

        return Response(data, status=status.HTTP_200_OK)


#BALANCE POR CUENTA
# Esta vista es para listar balance de una cuenta solo por mes.
class ListBalanceAccountMonthView(APIView):
    permission_classes=(IsAuthenticated,)
    
    def get(self, request, pk, month):
        ingresos_list = Move.objects.filter(day__month=month, concept__type_movement='ingreso', status_delete=False, account__id=pk, concept__user=request.user)
        ingresos_total = Move.objects.filter(day__month=month, concept__type_movement='ingreso', status_delete=False, account__id=pk, concept__user=request.user).aggregate(Sum('amount'))
        gastos_list = Move.objects.filter(day__month=month, concept__type_movement='gasto', status_delete=False, account__id=pk, concept__user=request.user)
        gastos_total = Move.objects.filter(day__month=month, concept__type_movement='gasto', status_delete=False, account__id=pk, concept__user=request.user).aggregate(Sum('amount'))
        serializer_ingresos = BalanceMoveSerializer(ingresos_list, many=True)
        serializer_gastos = BalanceMoveSerializer(gastos_list, many=True)
      
        balance = 0
        ingresos = ingresos_total.get("amount__sum", None)
        gastos = gastos_total.get("amount__sum", None)
        if ingresos is not None and gastos is not None:
            balance = ingresos-gastos
            data = { "account_incomes" : serializer_ingresos.data,
                     "account_spents" : serializer_gastos.data,
                     "balance": balance}
            return Response(data, status=status.HTTP_200_OK)
        elif ingresos is None and gastos is None:
            return Response({'No hay ingresos y tampoco gastos'}, status=status.HTTP_200_OK)        
        elif ingresos is None:
            balance = balance-gastos
            data = {
                "Message" : "No hay ingresos en este periodo",
                "account_spents" : serializer_gastos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)
        elif gastos is None:
            balance = balance+ingresos
            data = {
                "Message" : "No hay gastos en este periodo",
                "account_incomes" : serializer_ingresos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)

class ListBalanceAccountMonthYearView(APIView):
    permission_classes=(IsAuthenticated,)
    
    def get(self, request, pk, month, year):
        ingresos_list = Move.objects.filter(day__month=month, day__year=year, concept__type_movement='ingreso', status_delete=False, account__id=pk, concept__user=request.user)
        ingresos_total = Move.objects.filter(day__month=month, day__year=year, concept__type_movement='ingreso', status_delete=False, account__id=pk, concept__user=request.user).aggregate(Sum('amount'))
        gastos_list = Move.objects.filter(day__month=month, day__year=year, concept__type_movement='gasto', status_delete=False, account__id=pk, concept__user=request.user)
        gastos_total = Move.objects.filter(day__month=month, day__year=year, concept__type_movement='gasto', status_delete=False, account__id=pk, concept__user=request.user).aggregate(Sum('amount'))
        serializer_ingresos = BalanceMoveSerializer(ingresos_list, many=True)
        serializer_gastos = BalanceMoveSerializer(gastos_list, many=True)
      
        balance = 0
        ingresos = ingresos_total.get("amount__sum", None)
        gastos = gastos_total.get("amount__sum", None)
        if ingresos is not None and gastos is not None:
            balance = ingresos-gastos
            data = { "account_incomes" : serializer_ingresos.data,
                     "account_spents" : serializer_gastos.data,
                     "balance": balance}
            return Response(data, status=status.HTTP_200_OK)
        elif ingresos is None and gastos is None:
            return Response({'No hay ingresos y tampoco gastos'}, status=status.HTTP_200_OK)        
        elif ingresos is None:
            balance = balance-gastos
            data = {
                "Message" : "No hay ingresos en este periodo",
                "account_spents" : serializer_gastos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)
        elif gastos is None:
            balance = balance+ingresos
            data = {
                "Message" : "No hay gastos en este periodo",
                "account_incomes" : serializer_ingresos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)

# Esta vista es para listar balance de una cuenta por año.
class ListBalanceAccountYearView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, pk, year):
        ingresos_list = Move.objects.filter(day__year=year, concept__type_movement='ingreso', status_delete=False, account__id=pk, concept__user=request.user)
        ingresos_total = Move.objects.filter(day__year=year, concept__type_movement='ingreso', status_delete=False, account__id=pk, concept__user=request.user).aggregate(Sum('amount'))
        gastos_list = Move.objects.filter(day__year=year, concept__type_movement='gasto', status_delete=False, account__id=pk, concept__user=request.user)
        gastos_total = Move.objects.filter(day__year=year, concept__type_movement='gasto', status_delete=False, account__id=pk, concept__user=request.user).aggregate(Sum('amount'))
        serializer_ingresos = BalanceMoveSerializer(ingresos_list, many=True)
        serializer_gastos = BalanceMoveSerializer(gastos_list, many=True)
      
        balance = 0
        ingresos = ingresos_total.get("amount__sum", None)
        gastos = gastos_total.get("amount__sum", None)
        if ingresos is not None and gastos is not None:
            balance = ingresos-gastos
            data = { "account_incomes" : serializer_ingresos.data,
                     "account_spents" : serializer_gastos.data,
                     "balance": balance}
            return Response(data, status=status.HTTP_200_OK)
        elif ingresos is None and gastos is None:
            return Response({'No hay ingresos y tampoco gastos'}, status=status.HTTP_200_OK)        
        elif ingresos is None:
            balance = balance-gastos
            data = {
                "Message" : "No hay ingresos en este periodo",
                "account_spents" : serializer_gastos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)
        elif gastos is None:
            balance = balance+ingresos
            data = {
                "Message" : "No hay gastos en este periodo",
                "account_incomes" : serializer_ingresos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)

# Esta vista es para listar balance de una cuenta semana del año.
class ListBalanceAccountWeekView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, pk, week):
        ingresos_list = Move.objects.filter(day__week=week, concept__type_movement='ingreso', status_delete=False, account__id=pk, concept__user=request.user)
        ingresos_total = Move.objects.filter(day__week=week, concept__type_movement='ingreso', status_delete=False, account__id=pk, concept__user=request.user).aggregate(Sum('amount'))
        gastos_list = Move.objects.filter(day__week=week, concept__type_movement='gasto', status_delete=False, account__id=pk, concept__user=request.user)
        gastos_total = Move.objects.filter(day__week=week, concept__type_movement='gasto', status_delete=False, account__id=pk, concept__user=request.user).aggregate(Sum('amount'))
        serializer_ingresos = BalanceMoveSerializer(ingresos_list, many=True)
        serializer_gastos = BalanceMoveSerializer(gastos_list, many=True)
      
        balance = 0
        ingresos = ingresos_total.get("amount__sum", None)
        gastos = gastos_total.get("amount__sum", None)
        if ingresos is not None and gastos is not None:
            balance = ingresos-gastos
            data = { "account_incomes" : serializer_ingresos.data,
                     "account_spents" : serializer_gastos.data,
                     "balance": balance}
            return Response(data, status=status.HTTP_200_OK)
        elif ingresos is None and gastos is None:
            return Response({'No hay ingresos y tampoco gastos'}, status=status.HTTP_200_OK)        
        elif ingresos is None:
            balance = balance-gastos
            data = {
                "Message" : "No hay ingresos en este periodo",
                "account_spents" : serializer_gastos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)
        elif gastos is None:
            balance = balance+ingresos
            data = {
                "Message" : "No hay gastos en este periodo",
                "account_incomes" : serializer_ingresos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)

class ListBalanceAccountWeekYearView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, pk, week, year):
        ingresos_list = Move.objects.filter(day__week=week, day__year=year, concept__type_movement='ingreso', status_delete=False, account__id=pk, concept__user=request.user)
        ingresos_total = Move.objects.filter(day__week=week, day__year=year, concept__type_movement='ingreso', status_delete=False, account__id=pk, concept__user=request.user).aggregate(Sum('amount'))
        gastos_list = Move.objects.filter(day__week=week, day__year=year, concept__type_movement='gasto', status_delete=False, account__id=pk, concept__user=request.user)
        gastos_total = Move.objects.filter(day__week=week, day__year=year, concept__type_movement='gasto', status_delete=False, account__id=pk, concept__user=request.user).aggregate(Sum('amount'))
        serializer_ingresos = BalanceMoveSerializer(ingresos_list, many=True)
        serializer_gastos = BalanceMoveSerializer(gastos_list, many=True)
      
        balance = 0
        ingresos = ingresos_total.get("amount__sum", None)
        gastos = gastos_total.get("amount__sum", None)
        if ingresos is not None and gastos is not None:
            balance = ingresos-gastos
            data = { "account_incomes" : serializer_ingresos.data,
                     "account_spents" : serializer_gastos.data,
                     "balance": balance}
            return Response(data, status=status.HTTP_200_OK)
        elif ingresos is None and gastos is None:
            return Response({'No hay ingresos y tampoco gastos'}, status=status.HTTP_200_OK)        
        elif ingresos is None:
            balance = balance-gastos
            data = {
                "Message" : "No hay ingresos en este periodo",
                "account_spents" : serializer_gastos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)
        elif gastos is None:
            balance = balance+ingresos
            data = {
                "Message" : "No hay gastos en este periodo",
                "account_incomes" : serializer_ingresos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)


# Esta vista es para listar balance de una cuenta por día del año.
class ListBalanceAccountDayView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, pk, day):
        ingresos_list = Move.objects.filter(day=day, concept__type_movement='ingreso', status_delete=False, account__id=pk, concept__user=request.user)
        ingresos_total = Move.objects.filter(day=day, concept__type_movement='ingreso', status_delete=False, account__id=pk, concept__user=request.user).aggregate(Sum('amount'))
        gastos_list = Move.objects.filter(day=day, concept__type_movement='gasto', status_delete=False, account__id=pk, concept__user=request.user)
        gastos_total = Move.objects.filter(day=day, concept__type_movement='gasto', status_delete=False, account__id=pk, concept__user=request.user).aggregate(Sum('amount'))
        serializer_ingresos = BalanceMoveSerializer(ingresos_list, many=True)
        serializer_gastos = BalanceMoveSerializer(gastos_list, many=True)

        balance = 0
        ingresos = ingresos_total.get("amount__sum", None)
        gastos = gastos_total.get("amount__sum", None)
        if ingresos is not None and gastos is not None:
            balance = ingresos-gastos
            data = { "account_incomes" : serializer_ingresos.data,
                     "account_spents" : serializer_gastos.data,
                     "balance": balance}
            return Response(data, status=status.HTTP_200_OK)
        elif ingresos is None and gastos is None:
            return Response({'No hay ingresos y tampoco gastos'}, status=status.HTTP_200_OK)        
        elif ingresos is None:
            balance = balance-gastos
            data = {
                "Message" : "No hay ingresos en este periodo",
                "account_spents" : serializer_gastos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)
        elif gastos is None:
            balance = balance+ingresos
            data = {
                "Message" : "No hay gastos en este periodo",
                "account_incomes" : serializer_ingresos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)



# Esta vista es para listar balance de una cuenta con ingresos y gastos.
class ListBalanceAccountMoveView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, pk):
        ingresos_list = Move.objects.filter(concept__type_movement='ingreso', status_delete=False, account__id=pk, concept__user=request.user)
        ingresos_total = Move.objects.filter(concept__type_movement='ingreso', status_delete=False, account__id=pk, concept__user=request.user).aggregate(Sum('amount'))
        gastos_list = Move.objects.filter(concept__type_movement='gasto', status_delete=False, account__id=pk, concept__user=request.user)
        gastos_total = Move.objects.filter(concept__type_movement='gasto', status_delete=False, account__id=pk, concept__user=request.user).aggregate(Sum('amount'))
        serializer_ingresos = BalanceMoveSerializer(ingresos_list, many=True)
        serializer_gastos = BalanceMoveSerializer(gastos_list, many=True)
      
        balance = 0
        ingresos = ingresos_total.get("amount__sum", None)
        gastos = gastos_total.get("amount__sum", None)
        if ingresos is not None and gastos is not None:
            balance = ingresos-gastos
            data = { "account_incomes" : serializer_ingresos.data,
                     "account_spents" : serializer_gastos.data,
                     "balance": balance}
            return Response(data, status=status.HTTP_200_OK)
        elif ingresos is None and gastos is None:
            return Response({'No hay ingresos y tampoco gastos'}, status=status.HTTP_200_OK)        
        elif ingresos is None:
            balance = balance-gastos
            data = {
                "Message" : "No hay ingresos en este periodo",
                "account_spents" : serializer_gastos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)
        elif gastos is None:
            balance = balance+ingresos
            data = {
                "Message" : "No hay gastos en este periodo",
                "account_incomes" : serializer_ingresos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)

# Esta vista es para listar balance de una cuenta (gastos y los ingresos) fijos.
class ListBalanceAccountFixedMoveView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, pk):
        ingresos_list = Move.objects.filter(concept__type_clasification='fijo', concept__type_movement='ingreso', status_delete=False, account__id=pk, concept__user=request.user)
        ingresos_total = Move.objects.filter(concept__type_clasification='fijo', concept__type_movement='ingreso', status_delete=False, account__id=pk, concept__user=request.user).aggregate(Sum('amount'))
        gastos_list = Move.objects.filter(concept__type_clasification='fijo', concept__type_movement='gasto', status_delete=False, account__id=pk, concept__user=request.user)
        gastos_total = Move.objects.filter(concept__type_clasification='fijo', concept__type_movement='gasto', status_delete=False, account__id=pk, concept__user=request.user).aggregate(Sum('amount'))
        serializer_ingresos = BalanceMoveSerializer(ingresos_list, many=True)
        serializer_gastos = BalanceMoveSerializer(gastos_list, many=True)
      
        balance = 0
        ingresos = ingresos_total.get("amount__sum", None)
        gastos = gastos_total.get("amount__sum", None)
        if ingresos is not None and gastos is not None:
            balance = ingresos-gastos
            data = { "account_incomes" : serializer_ingresos.data,
                     "account_spents" : serializer_gastos.data,
                     "balance": balance}
            return Response(data, status=status.HTTP_200_OK)
        elif ingresos is None and gastos is None:
            return Response({'No hay ingresos y tampoco gastos'}, status=status.HTTP_200_OK)        
        elif ingresos is None:
            balance = balance-gastos
            data = {
                "Message" : "No hay ingresos en este periodo",
                "account_spents" : serializer_gastos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)
        elif gastos is None:
            balance = balance+ingresos
            data = {
                "Message" : "No hay gastos en este periodo",
                "account_incomes" : serializer_ingresos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)

# Esta vista es para listar balance (gastos y los ingresos) variables.
class ListBalanceAccountVariableMoveView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, pk):
        ingresos_list = Move.objects.filter(concept__type_clasification='variable', concept__type_movement='ingreso', status_delete=False, account__id=pk, concept__user=request.user)
        ingresos_total = Move.objects.filter(concept__type_clasification='variable', concept__type_movement='ingreso', status_delete=False, account__id=pk, concept__user=request.user).aggregate(Sum('amount'))
        gastos_list = Move.objects.filter(concept__type_clasification='variable', concept__type_movement='gasto', status_delete=False, account__id=pk, concept__user=request.user)
        gastos_total = Move.objects.filter(concept__type_clasification='variable', concept__type_movement='gasto', status_delete=False, account__id=pk, concept__user=request.user).aggregate(Sum('amount'))
        serializer_ingresos = BalanceMoveSerializer(ingresos_list, many=True)
        serializer_gastos = BalanceMoveSerializer(gastos_list, many=True)
      
        balance = 0
        ingresos = ingresos_total.get("amount__sum", None)
        gastos = gastos_total.get("amount__sum", None)
        if ingresos is not None and gastos is not None:
            balance = ingresos-gastos
            data = { "account_incomes" : serializer_ingresos.data,
                     "account_spents" : serializer_gastos.data,
                     "balance": balance}
            return Response(data, status=status.HTTP_200_OK)
        elif ingresos is None and gastos is None:
            return Response({'No hay ingresos y tampoco gastos'}, status=status.HTTP_200_OK)        
        elif ingresos is None:
            balance = balance-gastos
            data = {
                "Message" : "No hay ingresos en este periodo",
                "account_spents" : serializer_gastos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)
        elif gastos is None:
            balance = balance+ingresos
            data = {
                "Message" : "No hay gastos en este periodo",
                "account_incomes" : serializer_ingresos.data,
                "balance" : balance
            }
            return Response(data, status=status.HTTP_200_OK)

# Esta vista es para listar el balance de gastos de una cuenta.
class ListBalanceAccountSpentView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, pk):
        gastos_list = Move.objects.filter(concept__type_movement='gasto', status_delete=False, account__id=pk, concept__user=request.user)
        gastos_total = Move.objects.filter(concept__type_movement='gasto', status_delete=False, account__id=pk, concept__user=request.user).aggregate(Sum('amount'))
        serializer_gastos = BalanceMoveSerializer(gastos_list, many=True)
      
        data = { "account_spents" : serializer_gastos.data,
        "balance": gastos_total
        }

        return Response(data, status=status.HTTP_200_OK)

# Esta vista es para listar el balance de ingresos de una cuenta.
class ListBalanceAccountIncomeView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, pk):
        ingresos_list = Move.objects.filter(concept__type_clasification='variable', concept__type_movement='ingreso', status_delete=False, account__id=pk, concept__user=request.user)
        ingresos_total = Move.objects.filter(concept__type_clasification='variable', concept__type_movement='ingreso', status_delete=False, account__id=pk, concept__user=request.user).aggregate(Sum('amount'))
        serializer_ingresos = BalanceMoveSerializer(ingresos_list, many=True)
           
        data = { "account_incomes" : serializer_ingresos.data,
                 "balance": ingresos_total
        }

        return Response(data, status=status.HTTP_200_OK)
