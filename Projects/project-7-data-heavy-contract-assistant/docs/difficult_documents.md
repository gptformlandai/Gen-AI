# Example Difficult Documents

## Master Services Agreement

Difficulty:

- liability cap has an exception;
- confidentiality survives termination;
- governing law appears in metadata and clause text;
- obligations are party-specific.

Handling:

- parser extracts metadata separately;
- clause index keeps section paths;
- obligation extractor captures `Customer shall` and `Vendor shall` statements.

## Data Processing Addendum

Difficulty:

- breach notification has a precise 72-hour time limit;
- subprocessor obligations include advance notice;
- deletion obligations occur after termination.

Handling:

- clause retrieval is boosted for actor and topic terms;
- answer citations preserve document and section path.

## Service Level Agreement

Difficulty:

- service levels are stored in a table;
- remedies are row-specific;
- support response times use severity labels.

Handling:

- markdown tables are parsed into typed table rows;
- table rows become independent retrievable elements;
- answers cite table row IDs rather than broad sections.
