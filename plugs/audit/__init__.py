def need_audit(tablename):
    from uliweb import settings
    
    return tablename in settings.get_var('AUDIT/TABLES', [])

def post_save(sender, instance, created, data, old_data):
    from uliweb.orm import get_model
    import pickle
    from datetime import datetime
    from uliweb import request
    
    tablename = sender.tablename
    if not need_audit(tablename):
        return

    Audit = get_model('audit')
    Tables = get_model('tables')
    
    table = Tables.get_table(tablename)
    changed_value = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
    if created:
        modify_flag = '1'
        old_value = ''
    else:
        old = {}
        modify_flag = '2'
        for k in data.iterkeys():
            old[k] = old_data[k]
        old_value = pickle.dumps(old, pickle.HIGHEST_PROTOCOL)
        
    obj = Audit(table_id=table, obj_id=instance.id, changed_value=changed_value,
        old_value=old_value, modified_date=datetime.now(), modified_user=request.user,
        modify_flag=modify_flag, title=unicode(instance))
        
    obj.save()
    
def pre_delete(sender, instance):
    from uliweb.orm import get_model
    import pickle
    from datetime import datetime
    from uliweb import request
    
    tablename = sender.tablename
    if not need_audit(tablename):
        return

    Audit = get_model('audit')
    Tables = get_model('tables')
    
    table = Tables.get_table(tablename)
    changed_value = ''
    old_value = pickle.dumps(instance.to_dict(), pickle.HIGHEST_PROTOCOL)
    modify_flag = '3'
        
    obj = Audit(table_id=table, obj_id=instance.id, changed_value=changed_value,
        old_value=old_value, modified_date=datetime.now(), modified_user=request.user,
        modify_flag=modify_flag, title=unicode(instance))
        
    obj.save()
    