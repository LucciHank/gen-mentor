# Seed Knowledge Base - Demo MVP

Bộ dữ liệu này được thiết kế cho MVP hệ thống đào tạo nội bộ có các bước:
1. Upload tài liệu gốc vào object storage.
2. Parse về markdown/text/JSON.
3. Gắn metadata và index vào vector store / keyword index.
4. Dùng retrieval để phục vụ diagnostic test, learning path, lesson generation và tutor.
5. Lưu role-skill-course-assessment logic trong database quan hệ.

## Cấu trúc thư mục
- `raw/`: file gốc theo đúng định dạng docx/pdf/xlsx.
- `taxonomy/`: role list, skill list, level rubric, role-skill requirements.
- `metadata/`: manifest để ingest.
- `normalized_examples/`: ví dụ JSON sau khi chuẩn hóa.
- `database/`: schema SQL tối thiểu.
- `docs/`: hướng dẫn build nhanh.

## Hướng ingest đề xuất
### DOCX/PDF
- parse text
- tách heading / section
- chunk 300-800 tokens
- lưu vào `document_chunks`

### XLSX
- convert từng sheet / row group sang JSON
- map cột theo schema
- lưu master data vào bảng quan hệ
- chỉ index vector nếu sheet chứa FAQ / policy text dài

## Cách dùng tài liệu
- `lesson` / `sop` / `faq` / `checklist`: dùng cho tutor, lesson generator, assessment support
- `skill_matrix` / `course_mapping`: dùng cho learning path engine và validation
- `assessment_bank` / `rubric`: dùng cho test generator và scorer

## Build order gợi ý
1. Dùng file trong `taxonomy/` để seed DB.
2. Dùng `document_registry.csv` để tạo bản ghi documents.
3. Parse file trong `raw/`.
4. Chuyển output parse về format ở `normalized_examples/`.
5. Gắn chunks vào vector store.
6. Tạo retrieval APIs:
   - search_knowledge(query, filters)
   - get_role_requirements(role_id)
   - get_course_graph(skill_ids)
   - get_assessment_items(skill_ids, level)