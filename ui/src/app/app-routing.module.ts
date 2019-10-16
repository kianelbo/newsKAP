import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { IndexComponent } from './index/index.component';
import { SearchComponent } from './search/search.component';

const routes: Routes = [
  { path: '', component: IndexComponent },
  { path: 'index', redirectTo: '', pathMatch: 'full' },
  { path: 'search', component: SearchComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
