import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { IndexComponent } from './index/index.component';
import { SearchComponent } from './search/search.component';
import { ViewNewsComponent } from './view-news/view-news.component';

const routes: Routes = [
  { path: '', component: IndexComponent },
  { path: 'index', redirectTo: '', pathMatch: 'full' },
  { path: 'search', component: SearchComponent },
  { path: 'view/:id', component: ViewNewsComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
