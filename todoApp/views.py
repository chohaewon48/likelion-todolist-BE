from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from .models import Todo, User
from .serializers import TodoSerializer

# Create your views here.
class Todos(APIView):
    # 아까 작성한 거랑 이름만 같지 다른 함수임
    def get_user(self, user_id):
        try:
            user = User.objects.get(id = user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")    
        return user
    
    # 투두 리스트 조회
    def get(self, requset, user_id):
        # 유저 가져오기
        user = self.get_user(user_id)

        # 기본적으로 전체 Todo 리스트 조회
        todos = Todo.objects.filter(user=user)

        # 퀄 파라미터에서 month, day 가져오기
        month = requset.query_params.get("month")
        day = requset.query_params.get("day")

        # month, day가 둘 다 제공된 경우만 필터링
        if month is not None and day is not None:
            try:
                month = int(month)
                day = int(day)
                todos = todos.filter(date_month=month, date_dat=day)
            except ValueError:
                raise ParseError("month와 day는 정수여야 합니다.")
            
        # 정렬 및 추가 핉터링을 위한 sor_by 파라미터 가져오기
        sort_by = requset.query_params.get('sort_by', 'created_at')
        if sort_by not in ['created_at', 'updated_at']:
            sort_by = 'created_at'

        # 직렬화
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)