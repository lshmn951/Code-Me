from django.db import models
from django.contrib.postgres.fields import ArrayField


class User(models.Model):
    name = models.CharField(
        primary_key=True,
        max_length=20,
        verbose_name="사용자 이름"
    )
    rating = models.FloatField(
        verbose_name="평가 점수"
    )
    last_update = models.DateTimeField(
        verbose_name="레이팅 변동 날짜"
    )

    class Meta:
        db_table = "tb_user"
        ordering = ["-rating", "last_update"]


class Algorithm(models.Model):
    algorithm_id = models.AutoField(
        primary_key=True,
        verbose_name="알고리즘 번호"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="알고리즘 이름"
    )

    class Meta:
        db_table = "tb_algorithm"
        ordering = ["algorithm_id"]


class Problem(models.Model):
    number = models.IntegerField(
        primary_key=True,
        verbose_name="문제 번호"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="문제 이름"
    )
    algorithm_id = models.ForeignKey(
        "Algorithm",
        default=1,
        on_delete=models.CASCADE
    ) 
    submit = models.IntegerField(
        verbose_name="제출"
    )
    submit_people = models.IntegerField(
        verbose_name="제출한 사람"
    )
    accept_people = models.IntegerField(
        verbose_name="맞은 사람"
    )
    average_attempt = models.FloatField(
        verbose_name="평균 시도"
    )
    accept = models.IntegerField(
        verbose_name="맞았습니다"
    )
    wrong = models.IntegerField(
        verbose_name="틀렸습니다"
    )
    time_over = models.IntegerField(
        verbose_name="시간 초과"
    )
    memory_over = models.IntegerField(
        verbose_name="메모리 초과"
    )
    output_over = models.IntegerField(
        verbose_name="출력 초과"
    )
    output_type_error = models.IntegerField(
        verbose_name="출력 형식"
    )
    runtime_error = models.IntegerField(
        verbose_name="런타임 에러"
    )
    compile_error = models.IntegerField(
        verbose_name="컴파일 에러"
    )
    accept_proportion = models.FloatField(
        verbose_name="정답 비율"
    )
    accept_people_proportion = models.FloatField(
        verbose_name="정답자 비율"
    )

    class Meta:
        db_table = "tb_problem"
        ordering = ["number"]


class UserProblem(models.Model):
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE
    )
    problem = models.ForeignKey(
        "Problem",
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(fields=["user", "problem"], name="unique_user_problem_tuple")
        ]
        ordering = ["user"]


class UserSolvedProblem(UserProblem):
    class Meta:
        db_table = "tb_user_solved_problem"


class UserFailedProblem(UserProblem):
    class Meta:
        db_table = "tb_user_failed_problem"


class ProblemCounting(models.Model):
    problem = models.OneToOneField(
        "Problem",
        primary_key=True,
        on_delete=models.CASCADE
    )
    count_array = ArrayField(
        models.IntegerField(),
        verbose_name="문제 카운팅 배열"
    )

    class Meta:
        db_table = "tb_problem_counting"
        ordering = ["problem_id"]

