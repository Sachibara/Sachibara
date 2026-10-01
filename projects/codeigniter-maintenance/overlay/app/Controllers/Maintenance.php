<?php
namespace App\Controllers;
use App\Models\JobModel;
class Maintenance extends BaseController {
    public function index() {
        helper('form'); $status=$this->request->getGet('status'); $model=new JobModel();
        if(in_array($status,['Open','In Progress','Completed'],true))$model->where('status',$status);
        return view('maintenance',['jobs'=>$model->orderBy('id','DESC')->findAll(500),'filter'=>$status]);
    }
    public function create() {
        $rules=['equipment'=>'required|max_length[120]','issue'=>'required|max_length[1000]','priority'=>'required|in_list[Low,Medium,High]'];
        if(!$this->validate($rules))return redirect()->to('/')->with('errors',$this->validator->getErrors())->withInput();
        $data=$this->validator->getValidated(); $data['status']='Open'; (new JobModel())->insert($data);
        return redirect()->to('/')->with('notice','Maintenance job created.');
    }
    public function status($id) {
        $model=new JobModel(); if(!$model->find($id))throw \CodeIgniter\Exceptions\PageNotFoundException::forPageNotFound();
        if(!$this->validate(['status'=>'required|in_list[Open,In Progress,Completed]']))return redirect()->to('/')->with('errors',$this->validator->getErrors());
        $model->update($id,['status'=>$this->validator->getValidated()['status']]); return redirect()->to('/')->with('notice','Status updated.');
    }
}
