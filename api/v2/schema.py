import graphene
from graphene_django import DjangoObjectType
from polls.models import Question, Choice


# Types
class ChoiceType(DjangoObjectType):
    class Meta:
        model = Choice
        fields = ("id", "choice_text", "votes")


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("id", "question_text", "pub_date", "choices")


# Queries
class Query(graphene.ObjectType):
    all_questions = graphene.List(QuestionType)
    question = graphene.Field(QuestionType, id=graphene.Int(required=True))

    def resolve_all_questions(root, info):
        return Question.objects.all().order_by("-pub_date")

    def resolve_question(root, info, id):
        try:
            return Question.objects.get(pk=id)
        except Question.DoesNotExist:
            return None


# Mutations
class VoteMutation(graphene.Mutation):
    class Arguments:
        question_id = graphene.Int(required=True)
        choice_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    question = graphene.Field(QuestionType)

    def mutate(root, info, question_id, choice_id):
        try:
            question = Question.objects.get(pk=question_id)
            choice = question.choice_set.get(pk=choice_id)
            choice.votes += 1
            choice.save()
            return VoteMutation(ok=True, question=question)
        except (Question.DoesNotExist, Choice.DoesNotExist):
            return VoteMutation(ok=False, question=None)


class Mutation(graphene.ObjectType):
    vote = VoteMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
