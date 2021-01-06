import { Component, OnInit, ViewChild } from '@angular/core';

import { CanvasComponent } from '../../components/canvas/canvas.component';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss'],
})
export class HomePageComponent implements OnInit {
  @ViewChild('canvas') canvas: CanvasComponent;

  totalWidthL: number;
  totalWidthR: number;
  customer: string;
  orderNumber: string;

  glassType = 'klart';
  leftMount = 'wallmount';
  rightMount = 'post';
  globalWidth = 60;
  globalHeight = 60;
  transport = 'sendes';

  individualWidth: number;
  individualHeight: number;
  secondGlassHeight: number;

  packageList: any;
  totalWeight: number;

  constructor() {}

  ngOnInit(): void {}

  onSave() {
    // TODO
    // console.log('Save...');
  }

  onLoad() {
    // TODO
    // console.log('Load...');
  }

  onReset = () => this.canvas.clear();

  onUndo = () => this.canvas.undo();

  onAddWallmount = () => this.canvas.addWallmount();

  onAddPost = () => this.canvas.addPost();

  onAddGlass = () => this.canvas.addGlass();

  onAddGlassPolygon = () => this.canvas.addGlass(this.secondGlassHeight);
}
