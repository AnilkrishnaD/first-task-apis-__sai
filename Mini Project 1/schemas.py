from marshmallow import Schema, fields

class QuestionSchema(Schema):
    id = fields.Int(dump_only=True)
    question = fields.Str(required=True)
    question_type = fields.Str(required=True)

class QuestionUpdateSchema(Schema):
    question = fields.Str()
    question_type = fields.Str()
