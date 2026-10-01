/* Scripted REST resource: GET /changes; require authentication and REST_Endpoint ACL. */
(function process(request, response) {
    if (!gs.hasRole('u_sachi_change.operator')) { response.setStatus(403); response.setBody({error:'Operator role required'}); return; }
    var status=String(request.queryParams.status || '');
    if (status && ['draft','approved','rejected','implemented'].indexOf(status) === -1) {
        response.setStatus(400); response.setBody({error:'Invalid status'}); return;
    }
    var rows=[];
    var gr=new GlideRecordSecure('u_sachi_change');
    if (status) gr.addQuery('u_status',status);
    gr.orderByDesc('sys_created_on'); gr.setLimit(100); gr.query();
    while (gr.next()) rows.push({id:gr.getUniqueValue(),title:gr.getValue('u_title'),risk:gr.getValue('u_risk'),status:gr.getValue('u_status'),requested_by:gr.getDisplayValue('u_requested_by')});
    response.setBody({results:rows,limit:100});
})(request,response);
