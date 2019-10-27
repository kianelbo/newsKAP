import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService, NewsMiniItem } from '../services/api.service';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
  newsList: NewsMiniItem[];

  constructor(private route: ActivatedRoute,
              private apiService: ApiService) { }

  ngOnInit() {
    const queryStr = this.route.snapshot.queryParamMap.get('q');
    this.apiService.getResults(queryStr).subscribe(res => this.newsList = res);
  }

}
