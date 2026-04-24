# PHASE A - Xây kho tri thức

## Step A1 - Chuẩn hóa taxonomy
- roles.json
- skills.json
- levels.json
- assessment_types.json
- role_skill_requirements.json
- courses.json

## Step A2 - Upload file gốc
Ném toàn bộ thư mục `raw/` vào storage, đồng thời ghi bản ghi documents từ `metadata/document_registry.csv`.

## Step A3 - Parse và canonicalize
- DOCX/PDF -> markdown hoặc text theo heading
- XLSX -> JSON rows

## Step A4 - Gắn metadata
Dùng `metadata/knowledge_manifest.json`.

## Step A5 - Index
- FAQ / SOP / handbook / lesson -> vector index
- Course mapping / skill matrix / rubric -> relational DB + keyword lookup

## Step A6 - Build retrieval tools
- search_knowledge
- get_document_chunk
- get_role_requirements
- get_assessment_items
- get_course_graph

## Step A7 - Nối với LLM
Gemini chỉ gọi tool để lấy đúng tri thức; không để model tự nhớ nội dung nội bộ.