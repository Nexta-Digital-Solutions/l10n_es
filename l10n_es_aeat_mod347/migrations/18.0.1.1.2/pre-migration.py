import logging

_logger = logging.getLogger(__name__)

def _col_is_boolean(cr, table, column):
    cr.execute("""
        SELECT data_type
          FROM information_schema.columns
         WHERE table_name = %s
           AND column_name = %s
    """, (table, column))
    row = cr.fetchone()
    return row and row[0] == 'boolean'

def _convert_bool_to_jsonb(cr, table, column):
    # Odoo falla con ::jsonb, así que hacemos conversión segura.
    cr.execute(f"""
        ALTER TABLE "{table}"
        ALTER COLUMN "{column}" DROP DEFAULT
    """)
    cr.execute(f"""
        ALTER TABLE "{table}"
        ALTER COLUMN "{column}" TYPE jsonb
        USING to_jsonb("{column}")
    """)

def migrate(cr, version):
    # account_move.not_in_mod347
    if _col_is_boolean(cr, "account_move", "not_in_mod347"):
        _logger.info("Converting account_move.not_in_mod347 from boolean to jsonb (pre-upgrade).")
        _convert_bool_to_jsonb(cr, "account_move", "not_in_mod347")

    # res_partner.not_in_mod347
    if _col_is_boolean(cr, "res_partner", "not_in_mod347"):
        _logger.info("Converting res_partner.not_in_mod347 from boolean to jsonb (pre-upgrade).")
        _convert_bool_to_jsonb(cr, "res_partner", "not_in_mod347")
