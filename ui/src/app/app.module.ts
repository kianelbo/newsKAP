import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { IndexComponent } from './index/index.component';
import { QueryBarComponent } from './query-bar/query-bar.component';
import { SearchComponent } from './search/search.component';
import { ViewNewsComponent } from './view-news/view-news.component';

import { ApiService } from './services/api.service';

@NgModule({
  declarations: [
    AppComponent,
    IndexComponent,
    SearchComponent,
    QueryBarComponent,
    ViewNewsComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    AppRoutingModule
  ],
  providers: [ApiService],
  bootstrap: [AppComponent]
})
export class AppModule { }
