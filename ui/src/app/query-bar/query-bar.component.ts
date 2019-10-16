import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-query-bar',
  templateUrl: './query-bar.component.html',
  styleUrls: ['./query-bar.component.css']
})
export class QueryBarComponent implements OnInit {
  queryStr: string;

  constructor(private router: Router,
              private route: ActivatedRoute) { }

  ngOnInit() {
    this.queryStr = this.route.snapshot.queryParamMap.get('q');
  }

  clickSearch() {
    this.router.navigateByUrl('/search?q=' + this.queryStr);
  }
}
