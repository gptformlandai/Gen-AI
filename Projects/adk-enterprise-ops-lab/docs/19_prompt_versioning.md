# Prompt Versioning

Prompts live in `src/enterprise_ops_lab/prompts/`.

Recommended production fields:

- prompt name;
- version;
- owner;
- intended agent;
- eval suite required before release;
- rollback prompt version.

This project keeps prompts as Python constants for readability. Production systems can move them to checked YAML files.

