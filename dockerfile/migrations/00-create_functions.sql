CREATE OR REPLACE FUNCTION update_last_update()
  RETURNS TRIGGER AS $$
  BEGIN
      NEW.last_update = now();
      RETURN NEW;
  END;
  $$ language 'plpgsql';

