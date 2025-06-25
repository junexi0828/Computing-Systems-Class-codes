from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime

class TodoCreateSchema(Schema):
    """할 일 생성 스키마"""
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(allow_none=True)
    priority = fields.Str(validate=validate.OneOf(['높음', '중간', '낮음']), load_default='중간')
    category = fields.Str(validate=validate.OneOf(['개인', '업무', '학습']), load_default='개인')
    due_date = fields.DateTime(allow_none=True)
    is_public = fields.Bool(load_default=False)
    parent_id = fields.Int(allow_none=True)

class TodoUpdateSchema(Schema):
    """할 일 수정 스키마"""
    title = fields.Str(validate=validate.Length(min=1, max=200))
    description = fields.Str(allow_none=True)
    priority = fields.Str(validate=validate.OneOf(['높음', '중간', '낮음']))
    category = fields.Str(validate=validate.OneOf(['개인', '업무', '학습']))
    due_date = fields.DateTime(allow_none=True)
    is_public = fields.Bool()
    parent_id = fields.Int(allow_none=True)

class TodoResponseSchema(Schema):
    """할 일 응답 스키마"""
    id = fields.Int()
    user_id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    priority = fields.Str()
    category = fields.Str()
    due_date = fields.DateTime(allow_none=True)
    completed = fields.Bool()
    completed_at = fields.DateTime(allow_none=True)
    is_public = fields.Bool()
    parent_id = fields.Int(allow_none=True)
    tags = fields.List(fields.Dict(), load_default=[])
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class TodoListResponseSchema(Schema):
    """할 일 목록 응답 스키마"""
    todos = fields.List(fields.Nested(TodoResponseSchema))
    total = fields.Int()
    page = fields.Int()
    per_page = fields.Int()

class TodoFilterSchema(Schema):
    """할 일 필터 스키마"""
    search = fields.Str(allow_none=True)
    priority = fields.Str(validate=validate.OneOf(['높음', '중간', '낮음']), allow_none=True)
    category = fields.Str(validate=validate.OneOf(['개인', '업무', '학습']), allow_none=True)
    completed = fields.Bool(allow_none=True)
    due_date = fields.DateTime(allow_none=True)
    sort_by = fields.Str(validate=validate.OneOf(['created_at', 'updated_at', 'due_date', 'priority', 'title']), load_default='created_at')
    order = fields.Str(validate=validate.OneOf(['asc', 'desc']), load_default='desc')
    page = fields.Int(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Int(load_default=20, validate=validate.Range(min=1, max=100))