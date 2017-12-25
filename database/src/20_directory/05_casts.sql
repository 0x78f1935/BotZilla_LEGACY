CREATE FUNCTION directory.to_char(directory.pointset)
    RETURNS text
AS $$
    SELECT 'point.' || $1."name"
$$ LANGUAGE sql STABLE STRICT;

CREATE CAST (directory.pointset AS text)
  WITH FUNCTION directory.to_char(directory.pointset);
