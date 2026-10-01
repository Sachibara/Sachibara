/* Before Business Rule: u_sachi_change; Insert + Update; Advanced. */
(function executeRule(current, previous) {
    if (!gs.hasRole('u_sachi_change.operator')) {
        gs.addErrorMessage('Change operator role required.'); current.setAbortAction(true); return;
    }
    if (current.operation() === 'insert') {
        current.setValue('u_status','draft');
        current.setValue('u_requested_by',gs.getUserID());
        return;
    }
    var oldStatus=previous.getValue('u_status');
    var nextStatus=current.getValue('u_status');
    // Finalized records cannot silently change risk, description or plan.
    if ((oldStatus === 'rejected' || oldStatus === 'implemented') &&
        (current.u_risk.changes() || current.u_title.changes() || current.u_rollback_plan.changes())) {
        gs.addErrorMessage('Finalized changes are read-only.'); current.setAbortAction(true); return;
    }
    if (oldStatus === 'approved' && (current.u_risk.changes() || current.u_rollback_plan.changes() || current.u_title.changes())) {
        gs.addErrorMessage('Create a new draft to change an approved plan.'); current.setAbortAction(true); return;
    }
    if (!current.u_status.changes()) return;
    var hasPlan=(current.getValue('u_rollback_plan') || '').replace(/\s/g,'').length > 0;
    if (!(new ChangePolicy()).canTransition(oldStatus,nextStatus,current.getValue('u_risk'),hasPlan,gs.hasRole('u_sachi_change.approver'))) {
        gs.addErrorMessage('Invalid transition, missing approval role, or missing high-risk rollback plan.'); current.setAbortAction(true);
    }
})(current, previous);
