import {Component,inject} from '@angular/core';
import {bootstrapApplication} from '@angular/platform-browser';
import {HttpClient,provideHttpClient} from '@angular/common/http';
import {FormsModule} from '@angular/forms';
import {CommonModule} from '@angular/common';
interface Asset {id:number;tag:string;name:string;owner:string;status:string}
@Component({selector:'asset-app',standalone:true,imports:[FormsModule,CommonModule],template:`
<main><header><div><span class="eyebrow">Sachibara / Fullstack lab</span><h1>Asset lifecycle console</h1><p class="muted">A clear view of your equipment, ownership and lifecycle.</p></div><span class="badge">Angular × .NET</span></header>
<p *ngIf="error" class="error" role="alert">{{error}}</p><p *ngIf="loading" role="status">Loading assets…</p>
<div class="grid"><div class="card"><span class="muted">Total assets</span><div class="stat">{{assets.length}}</div></div><div class="card"><span class="muted">Available</span><div class="stat">{{count('Available')}}</div></div><div class="card"><span class="muted">In repair</span><div class="stat">{{count('Repair')}}</div></div></div>
<form class="inline" (ngSubmit)="save()"><label>Tag<br><input name="tag" required maxlength="40" [(ngModel)]="draft.tag"></label><label>Equipment<br><input name="name" required maxlength="120" [(ngModel)]="draft.name"></label><label>Owner<br><input name="owner" maxlength="80" [(ngModel)]="draft.owner"></label><label>Status<br><select name="status" [(ngModel)]="draft.status"><option *ngFor="let status of statuses">{{status}}</option></select></label><button [disabled]="saving">{{draft.id ? 'Update asset' : 'Add asset'}}</button><button type="button" class="secondary" (click)="reset()">Cancel</button></form>
<div class="toolbar"><label>Search tag, equipment or owner<br><input [(ngModel)]="query"></label><button class="secondary" (click)="load()" [disabled]="loading">Refresh</button></div>
<section class="panel table-wrap"><table><thead><tr><th>Tag</th><th>Equipment</th><th>Owner</th><th>Status</th><th>Actions</th></tr></thead><tbody><tr *ngFor="let a of filtered"><td>{{a.tag}}</td><td>{{a.name}}</td><td>{{a.owner || 'Unassigned'}}</td><td><span class="badge">{{a.status}}</span></td><td><button class="secondary" (click)="edit(a)" [disabled]="saving">Edit</button> <button class="danger" (click)="remove(a)" [disabled]="saving">Delete</button></td></tr></tbody></table><p *ngIf="!filtered.length">No matching assets. Add your first equipment record above.</p></section><footer>Local portfolio demo · EF Core + SQLite persistence</footer></main>`})
class App {
  private http=inject(HttpClient);assets:Asset[]=[];query='';error='';saving=false;loading=false;statuses=['Available','Assigned','Repair','Retired'];draft:Asset={id:0,tag:'',name:'',owner:'',status:'Available'};
  constructor(){this.load();}
  get filtered(){const q=this.query.toLowerCase();return this.assets.filter(a=>[a.tag,a.name,a.owner].some(v=>v.toLowerCase().includes(q)));}
  count(status:string){return this.assets.filter(a=>a.status===status).length;}
  load(){this.loading=true;this.http.get<Asset[]>('/api/assets').subscribe({next:rows=>{this.assets=rows;this.error='';this.loading=false;},error:()=>{this.error='API unavailable. Start the .NET server on port 5080.';this.loading=false;}});}
  edit(a:Asset){this.draft={...a};} reset(){this.draft={id:0,tag:'',name:'',owner:'',status:'Available'};}
  save(){if(this.saving)return;this.saving=true;const {id,...body}=this.draft;const req=id?this.http.put('/api/assets/'+id,body):this.http.post('/api/assets',body);req.subscribe({next:()=>{this.saving=false;this.reset();this.load();},error:e=>{this.saving=false;this.error=e.error?.error||'Save failed. Check all fields.';}});}
  remove(a:Asset){if(!confirm('Delete '+a.tag+'?'))return;this.saving=true;this.http.delete('/api/assets/'+a.id).subscribe({next:()=>{this.saving=false;if(this.draft.id===a.id)this.reset();this.load();},error:()=>{this.saving=false;this.error='Delete failed.';}});}
}
bootstrapApplication(App,{providers:[provideHttpClient()]}).catch(console.error);
