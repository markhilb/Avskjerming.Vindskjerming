import { Component } from '@angular/core';
import { animations } from './animations';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  animations: [animations],
})
export class AppComponent {
  title = 'vindskjerming';
}
