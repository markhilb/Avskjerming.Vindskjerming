import { Component, OnInit, Input, Output, ViewChild } from '@angular/core';

import { Item, Wallmount, Post, Glass } from '../../models/items.model';
import { WallComponent } from './wall/wall.component';

@Component({
  selector: 'app-canvas',
  templateUrl: './canvas.component.html',
  styleUrls: ['./canvas.component.scss'],
})
export class CanvasComponent implements OnInit {
  @ViewChild('leftWall') leftWall: WallComponent;
  @ViewChild('rightWall') rightWall: WallComponent;

  @Input() totalWidthL: number;
  @Input() totalWidthR: number;
  @Input() globalWidth: number;
  @Input() globalHeight: number;
  @Input() individualWidth: number;
  @Input() individualHeight: number;
  @Input() leftMount: string;
  @Input() rightMount: string;
  @Input() glassType: string;

  constructor() {}

  ngOnInit(): void {}

  addWallmount() {
    if (this.rightWall) {
      if (this.rightWall.items.length > 0) {
        // If the right wall is not empty, add wallmount there
        this.rightWall.addWallmount(this.individualHeight);
      } else {
        // If right wall is empty, try to add wallmount to left wall
        if (!this.leftWall.addWallmount(this.individualHeight))
          // If left wall is full, add to right wall
          this.rightWall.addWallmount(this.individualHeight);
      }
    } else if (this.leftWall) {
      this.leftWall.addWallmount(this.individualHeight);
    }
  }

  addPost() {
    if (this.rightWall) {
      if (this.rightWall.items.length > 0) {
        // If the right wall is not empty, add post there
        this.rightWall.addPost(this.individualHeight);
      } else {
        // If right wall is empty, try to add post to left wall
        if (!this.leftWall.addPost(this.individualHeight))
          // If left wall is full, add to right wall
          this.rightWall.addPost(this.individualHeight);
      }
    } else if (this.leftWall) {
      this.leftWall.addPost(this.individualHeight);
    }
  }

  addGlass(secondHeight = -1) {
    if (this.rightWall) {
      if (this.rightWall.items.length > 0) {
        // If the right wall is not empty, add glass there
        this.rightWall.addGlass(
          this.individualWidth,
          this.individualHeight,
          secondHeight,
        );
      } else {
        // If right wall is empty, try to add glass to left wall
        if (
          !this.leftWall.addGlass(
            this.individualWidth,
            this.individualHeight,
            secondHeight,
          )
        )
          // If left wall is full, add to right wall
          this.rightWall.addGlass(
            this.individualWidth,
            this.individualHeight,
            secondHeight,
          );
      }
    } else if (this.leftWall) {
      this.leftWall.addGlass(
        this.individualWidth,
        this.individualHeight,
        secondHeight,
      );
    }
  }

  clear() {
    if (this.leftWall) this.leftWall.clear();
    if (this.rightWall) this.rightWall.clear();
  }

  undo() {
    if (this.rightWall) this.rightWall.undo();
    else if (this.leftWall) this.leftWall.undo();
  }
}
