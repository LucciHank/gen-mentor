# API gợi ý cho bản demo tối giản

## Knowledge ingestion
- POST /documents/upload
- POST /documents/{id}/parse
- POST /documents/{id}/index
- GET /documents
- GET /documents/{id}

## Retrieval
- POST /knowledge/search
- GET /roles/{role_id}/requirements
- POST /courses/graph
- POST /assessment/items/search

## Learner intake
- POST /goals/refine
- POST /cv/parse
- POST /diagnostic/generate
- POST /diagnostic/submit
- POST /learner-profile/build
- POST /learning-path/generate
- POST /learning-path/reschedule

## Learning runtime
- POST /lesson/generate
- POST /quiz/generate
- POST /tutor/chat
- POST /learner-progress/update