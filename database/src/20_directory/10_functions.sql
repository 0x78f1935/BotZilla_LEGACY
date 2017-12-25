
--------------------
-- PointSet Creation
--------------------

CREATE OR REPLACE FUNCTION directory._new_pointset(character varying, integer)
  RETURNS directory.pointset AS
$$
  INSERT INTO directory.pointset(name, style_id) SELECT $1, $2 RETURNING pointset;
$$ LANGUAGE sql VOLATILE;

CREATE OR REPLACE FUNCTION directory._new_pointset_attributes(ps directory.pointset, attributes text[])
  RETURNS directory.pointset AS
$$
  INSERT INTO directory.pointset_attribute
    (pointset_id, name)
  SELECT ps.id, n
    FROM UNNEST($2) AS n;

  SELECT $1;
$$ LANGUAGE sql VOLATILE;

CREATE OR REPLACE FUNCTION directory._new_pointset_table(ps directory.pointset, attributes text[])
  RETURNS directory.pointset AS
$$
BEGIN
  EXECUTE format('CREATE TABLE point.%I (
          id SERIAL NOT NULL,
          position geometry NOT NULL,
          %s,
          PRIMARY KEY (id)
      )',
      $1.name,
      array_to_string((SELECT array_agg(quote_ident(a) || ' text') FROM UNNEST($2) AS a), ' ,')
    );
  RETURN $1;
END;
$$ LANGUAGE plpgsql VOLATILE;


CREATE OR REPLACE FUNCTION directory.create_pointset(name character varying, style_id integer, attributes text[])
  RETURNS directory.pointset AS
$$
  SELECT
    directory._new_pointset_table(
      directory._new_pointset_attributes(
        directory._new_pointset(name, style_id),
        attributes
      ),
      attributes
    );
$$ LANGUAGE sql VOLATILE;

